import os
from flask_restful import reqparse
from flask import current_app
from brainminer.base.api import HtmlResource
from brainminer.storage.dao import FileDao
from werkzeug.datastructures import FileStorage
from brainminer.base.util import generate_string
from brainminer.compute.dao import SessionDao


# ----------------------------------------------------------------------------------------------------------------------
class SessionFilesResource(HtmlResource):

    URI = '/sessions/{}/files'

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
        del args['file']

        f_dao = FileDao(self.db_session())
        f = f_dao.create(**args)
        session_dao = SessionDao(self.db_session())
        session = session_dao.retrieve(id=id)

        # Run training session. Should be done in a separate, asynchronous thread
        # but I don't feel like implementing it. The trained classifier should be persisted to file so that
        # it can be easily retrieved for prediction. Trained classifiers should also be listed in the home page so
        # you can reuse them. Ideally, they have a unique ID and human-readable description.
        print('Training SVM on {}'.format(f.name))
        session.training_file_path = f.storage_path
        session.classifier_file_path = '/path_to_classifier'

        html = '<h3>Thanks for uploading your file!</h3>'
        html += '<p>It has been uploaded to this location:</p>'
        html += '<p><a target="_blank" href="/files/{}/content">{}</a></p>'.format(f.id, f.storage_id)
        html += '<br>'
        html += '<p>Your classifier has been trained and is now ready to be used for predictions</p>'
        html += '<p>Upload a CSV file with your cases to be predicted below:</p>'
        html += '<form method="post" enctype="multipart/form-data" action="/sessions/{}/predictions">'.format(session.id)
        html += '  <input type="file" name="file">'
        html += '  <input type="submit" value="Upload predictions">'
        html += '</form>'

        return self.output_html(html, 201)


# ----------------------------------------------------------------------------------------------------------------------
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
        del args['file']

        f_dao = FileDao(self.db_session())
        f = f_dao.create(**args)
        session_dao = SessionDao(self.db_session())
        session = session_dao.retrieve(id=id)

        # Load classifier object file and run the prediction

        # Run the prediction. After it finishes we throw aways the prediction file.
        print('Running prediction...')

        html = '<h3>Congratulations! You have successfully completed your prediction!</h3'
        html += '<p>Here are the results:</p>'

        return self.output_html(html, 201)
