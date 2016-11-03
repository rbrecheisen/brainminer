import os
from flask import send_from_directory, current_app
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage
from brainminer.base.handlers import (
    ResourceListGetHandler, ResourceListPostHandler, ResourceGetHandler, ResourcePutHandler, ResourceDeleteHandler)
from brainminer.base.util import generate_string
from brainminer.storage.dao import RepositoryDao, FileDao, FileSetDao
from brainminer.storage.exceptions import FileNotInRepositoryException


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesGetHandler(ResourceListGetHandler):

    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repositories = repository_dao.retrieve_all(**args)
        result = [repository.to_dict() for repository in repositories]

        return result, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository')


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesPostHandler(ResourceListPostHandler):

    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.create(**args)

        return repository.to_dict(), 201

    def check_permissions(self):
        self.current_user().check_permission('create:repository')


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryGetHandler(ResourceGetHandler):

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())

        return repository.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryPutHandler(ResourcePutHandler):

    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())

        if args['name'] != repository.name:
            repository.name = args['name']

        repository_dao.save(repository)

        return repository.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('update:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryDeleteHandler(ResourceDeleteHandler):

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        repository_dao.delete(repository)

        return {}, 204

    def check_permissions(self):
        self.current_user().check_permission('delete:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFilesGetHandler(ResourceListGetHandler):
    
    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        result = [f.to_dict() for f in repository.files]

        return result, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFilesPostHandler(ResourceListPostHandler):
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True, location='form')
        parser.add_argument('modality', type=str, required=True, location='form')
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

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        f_dao = FileDao(self.db_session())

        f = f_dao.create(
            name=args['name'],
            type=args['type'],
            modality=args['modality'],
            extension=args['extension'],
            content_type=args['content_type'],
            size=args['size'],
            storage_id=args['storage_id'],
            storage_path=args['storage_path'],
            media_link=args['media_link'],
            repository=repository,
        )

        return f.to_dict(), 201

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('create:file')


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileGetHandler(ResourceGetHandler):

    def __init__(self, id, file_id):
        super(RepositoryFileGetHandler, self).__init__(id)
        self._file_id = file_id

    def file_id(self):
        return self._file_id

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=self.file_id())
        if f.repository != repository:
            raise FileNotInRepositoryException(f.name, repository.name)

        return f.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('retrieve:file@{}'.format(self.file_id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileContentGetHandler(ResourceGetHandler):

    def __init__(self, id, file_id):
        super(RepositoryFileContentGetHandler, self).__init__(id)
        self._file_id = file_id

    def file_id(self):
        return self._file_id

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=self.file_id())
        if f.repository != repository:
            raise FileNotInRepositoryException(f.name, repository.name)

        return send_from_directory(
            os.path.join(current_app.root_path, self.config()['UPLOAD_DIR']), filename=f.storage_id), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('retrieve:file@{}'.format(self.file_id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, file_id):
        super(RepositoryFileDeleteHandler, self).__init__(id)
        self._file_id = file_id

    def file_id(self):
        return self._file_id

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=self.file_id())
        if f.repository != repository:
            raise FileNotInRepositoryException(f.name, repository.name)
        f_dao.delete(f)

        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('delete:file@{}'.format(self.file_id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetsGetHandler(ResourceListGetHandler):

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetsPostHandler(ResourceListPostHandler):

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('create:file-set')


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetGetHandler(ResourceGetHandler):

    def __init__(self, id, file_set_id):
        super(RepositoryFileSetGetHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('retrieve:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetPutHandler(ResourcePutHandler):

    def __init__(self, id, file_set_id):
        super(RepositoryFileSetPutHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('update:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, file_set_id):
        super(RepositoryFileSetDeleteHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('delete:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFilesGetHandler(ResourceListGetHandler):

    def __init__(self, id, file_set_id):
        super(RepositoryFileSetFilesGetHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('retrieve:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFilePutHandler(ResourcePutHandler):

    def __init__(self, id, file_set_id):
        super(RepositoryFileSetFilePutHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('update:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFileDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, file_set_id):
        super(RepositoryFileSetFileDeleteHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('update:file-set@{}'.format(self.file_set_id()))
