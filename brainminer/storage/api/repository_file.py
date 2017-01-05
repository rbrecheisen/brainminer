import os
from flask_restful import reqparse
from flask import send_from_directory, current_app
from werkzeug.datastructures import FileStorage
from brainminer.base.util import generate_string
from brainminer.base.api import PermissionProtectedResource
from brainminer.storage.dao import RepositoryDao, FileDao
from brainminer.storage.exceptions import FileNotInRepositoryException


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFilesResource(PermissionProtectedResource):

    URI = '/repositories/{}/files'

    def get(self, id):

        self.check_permission('retrieve:repository@{}'.format(id))
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        # We only return those files in the repository that are accessible to the
        # current user. Normally, all files uploaded by the user will be accessible
        # and optionally other files that were shared with him.
        result = []
        # If the user has class-level retrieve permission for files, then we don't
        # have to check file permissions individually
        if self.has_permission('retrieve:file'):
            result = [f.to_dict() for f in repository.files]
        else:
            for f in repository.files:
                if self.has_permission('retrieve:file@{}'.format(f.id)):
                    result.append(f.to_dict())

        return result, 200

    def post(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, required=True, location='files')
        args = parser.parse_args()
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        args['repository'] = repository
        args['storage_id'] = generate_string()
        args['storage_path'] = os.path.join(current_app.root_path, self.config()['UPLOAD_DIR'], args['storage_id'])
        args['file'].save(args['storage_path'])
        args['name'] = args['file'].filename
        args['extension'] = '.'.join(args['name'].split('.')[1:])
        args['content_type'] = 'application/octet-stream'
        args['media_link'] = args['storage_path']
        args['size'] = 0
        # Remove 'file' element in the arguments because the File constructor
        # does not expect it
        del args['file']
        f_dao = FileDao(self.db_session())
        f = f_dao.create(**args)

        return f.to_dict(), 201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileResource(PermissionProtectedResource):

    URI = '/repositories/{}/files/{}'

    def get(self, id, file_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve:file@{}'.format(file_id))
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=file_id)
        if f.repository != repository:
            raise FileNotInRepositoryException(f.name, repository.name)

        return f.to_dict(), 200

    def delete(self, id, file_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve,delete:file@{}'.format(file_id))
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=file_id)
        if f.repository != repository:
            raise FileNotInRepositoryException(f.name, repository.name)
        f_dao.delete(f)

        return {}, 200


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileContentResource(PermissionProtectedResource):

    URI = '/repositories/{}/files/{}/content'

    def get(self, id, file_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve:file@{}'.format(file_id))
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=file_id)
        if f.repository != repository:
            raise FileNotInRepositoryException(f.name, repository.name)

        return send_from_directory(
            os.path.join(current_app.root_path, self.config()['UPLOAD_DIR']), filename=f.storage_id), 200
