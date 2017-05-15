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
        return self.output_html('Not implemented', 201)


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

        print('Running prediction...')

        # Load classifier object file and run the prediction

        # Run the prediction.
        
        # Delete CSV file
        
        html = '<h3>Congratulations!</h3>'
        html += '<p>You have successfully completed your prediction!</p>'
        html += '<p>Here are the results:</p>'

        return self.output_html(html, 201)
