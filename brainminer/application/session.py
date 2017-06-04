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
        html += '<p>Upload a CSV file below with cases to predict.</p>'

        html += '<form method="post" enctype="multipart/form-data" action="/sessions/{}/predictions">'.format(session.id)
        html += '  <input type="file" name="file">'
        html += '  <input type="submit" value="Upload predictions">'
        html += '</form>'

        return self.output_html(html, 200)


class SessionPredictionsResource(HtmlResource):

    URI = '/sessions/{}/predictions'

    def post(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, required=True, location='files')
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
        features = pd.read_csv(args['storage_path'])
        x = get_x(features)
        classifier = joblib.load(session.classifier_file_path)
        predictions = classifier.predict(x)

        html = ''
        html += '<p>Predictions:</p>'
        for p in predictions:
            html += '{}'.format(p)

        html += '<p>Click the button "Restart" to start over. You can train a new<br>'
        html += 'classifier or select an existing training session and run another<br>'
        html += 'prediction.</p>'
        html += '<form method="get" action="/">'
        html += '  <input type="submit" value="Restart">'
        html += '</form>'

        return self.output_html(html, 201)
