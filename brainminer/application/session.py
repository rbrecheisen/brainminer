import os
from werkzeug.datastructures import FileStorage
from flask_restful import reqparse
from flask import current_app
from brainminer.base.api import HtmlResource
from brainminer.compute.dao import SessionDao
from brainminer.base.util import generate_string, get_x
from brainminer.base.api import HtmlResource

import pandas as pd
from sklearn.externals import joblib


class SessionResource(HtmlResource):

     URI = '/sessions/{}'

     def get(self, id):

        session_dao = SessionDao(self.db_session())
        session = session_dao.retrieve(id=id)

        html = ''
        html += '<h3>Step 4 - Run predictions</h3>'
        html += '<p>Upload a CSV file below with cases to predict. Specify the label <br>'
        html += 'the column identifying your cases, e.g., SubjectID.</p>'

        html += '<form method="post" enctype="multipart/form-data" action="/sessions/{}/predictions">'.format(session.id)
        html += '  <input type="file" name="file"><br><br>'
        html += '  <input type="text" name="subject_id" value="MRid">Case identifier<br><br>'
        html += '  <input type="submit" value="Upload predictions">'
        html += '</form>'

        return self.output_html(html, 200)


class SessionPredictionsResource(HtmlResource):

    URI = '/sessions/{}/predictions'

    def post(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, required=True, location='files')
        parser.add_argument('subject_id', type=str, required=True, location='form')
        args = parser.parse_args()

        args['storage_id'] = generate_string()
        args['storage_path'] = os.path.join(current_app.root_path, self.config()['UPLOAD_DIR'], args['storage_id'])
        args['file'].save(args['storage_path'])
        args['name'] = args['file'].filename
        args['extension'] = '.'.join(args['name'].split('.')[1:])
        args['content_type'] = 'application/octet-stream'
        args['media_link'] = args['storage_path']
        args['size'] = 0

        # Get trained classifier from session
        session_dao = SessionDao(self.db_session())
        session = session_dao.retrieve(id=id)

        # Load features
        features = pd.read_csv(args['storage_path'], index_col=args['subject_id'])
        x = get_x(features)
        classifier = joblib.load(session.classifier_file_path)
        predictions = classifier.predict(x)

        html = ''
        html += '<h3>Congratulations!</h3>'
        html += '<p>You have successfully run one or more predictions. The results<br>'
        html += 'are listed below.</p>'
        html += '<table border="1">'
        html += '<tr><th>Case ID</th><th>Predicted target</th></tr>'

        for i in range(len(features.index)):
            html += '<tr><td>{}</td><td>{}</td></tr>'.format(features.index[i], predictions[i])

        html += '</table>'
        html += '<p>Click the button "Restart" to start over. You can train a new<br>'
        html += 'classifier or select an existing training session and run another<br>'
        html += 'prediction.</p>'
        html += '<form method="get" action="/">'
        html += '  <input type="submit" value="Restart">'
        html += '</form>'

        return self.output_html(html, 201)
