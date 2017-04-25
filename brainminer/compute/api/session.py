import os
from flask_restful import reqparse
from flask import current_app
from brainminer.base.api import BaseResource
from brainminer.storage.dao import FileDao
from werkzeug.datastructures import FileStorage
from brainminer.base.util import generate_string
from brainminer.compute.dao import SessionDao


# ----------------------------------------------------------------------------------------------------------------------
class SessionFilesResource(BaseResource):

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
        # but I don't feel like implementing it.
        print('Training SVM on {}'.format(f.name))
        session.object_file_path = '/path_to_classifier'

        return session.to_dict(), 201


# ----------------------------------------------------------------------------------------------------------------------
class SessionPredictionsResource(BaseResource):

    URI = '/sessions/{}/predictions'

    def post(self, id):
        return {}, 201
