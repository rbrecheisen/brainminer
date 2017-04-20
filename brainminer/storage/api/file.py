import os
from flask_restful import reqparse
from flask import send_from_directory, current_app
from werkzeug.datastructures import FileStorage
from brainminer.base.util import generate_string
from brainminer.base.api import BaseResource, HtmlResource
from brainminer.storage.dao import FileDao


# ----------------------------------------------------------------------------------------------------------------------
class FilesResource(HtmlResource):
    
    URI = '/files'
    
    def post(self):

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

        return self.output_html('''
        <h3>Thanks for uploading your file!</h3>
        <span>You can get it here: <a href="/files/{}/content">download</a></span>
        <br>
        <h3>To train a classifier with this file, click the following link:</h3>
        <a href="/train/{}">train classifier</a>
        <br>
        <h3>To run a prediction, click the following link:</h3>
        <a href="/predict/{}">train classifier</a>
        '''.format(f.id, f.id, f.id), 201)
    

# ----------------------------------------------------------------------------------------------------------------------
class FileResource(HtmlResource):
    
    URI = '/files/{}'
    
    def get(self, id):
        
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=id)

        return f.to_dict(), 200

    def delete(self, id):

        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=id)
        f_dao.delete(f)

        return self.output_html('<h3>Not implemented</h3', 200)


# ----------------------------------------------------------------------------------------------------------------------
class FileContentResource(BaseResource):
    
    URI = '/files/{}/content'
    
    def get(self, id):

        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=id)

        return send_from_directory(
            os.path.join(current_app.root_path, self.config()['UPLOAD_DIR']), filename=f.storage_id), 200
