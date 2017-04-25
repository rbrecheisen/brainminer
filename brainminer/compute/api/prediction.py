from flask_restful import reqparse
from brainminer.base.api import BaseResource
from brainminer.storage.dao import FileDao


# ----------------------------------------------------------------------------------------------------------------------
class PredictionFilesResource(BaseResource):

    URI = '/predictions/{}/files'

    def post(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('file_id', type=str, location='form')
        args = parser.parse_args()

        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=int(args['file_id']))

        return {}, 201
