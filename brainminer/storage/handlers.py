import os
from flask import send_from_directory, current_app
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage
from brainminer.base.handlers import (
    ResourceListRetrieveHandler, ResourceListCreateHandler, ResourceRetrieveHandler, ResourceUpdateHandler, ResourceDeleteHandler)
from brainminer.base.util import generate_string
from brainminer.storage.dao import RepositoryDao, FileDao, FileSetDao
from brainminer.storage.exceptions import FileNotInRepositoryException, FileSetNotInRepositoryException


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesRetrieveHandler(ResourceListRetrieveHandler):

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
class RepositoriesCreateHandler(ResourceListCreateHandler):

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
class RepositoryRetrieveHandler(ResourceRetrieveHandler):

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())

        return repository.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryUpdateHandler(ResourceUpdateHandler):

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
class FilesRetrieveHandler(ResourceListRetrieveHandler):
    
    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        result = [f.to_dict() for f in repository.files]

        return result, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class FilesCreateHandler(ResourceListCreateHandler):
    
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
class FileRetrieveHandler(ResourceRetrieveHandler):

    def __init__(self, id, file_id):
        super(FileRetrieveHandler, self).__init__(id)
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
class FileContentRetrieveHandler(ResourceRetrieveHandler):

    def __init__(self, id, file_id):
        super(FileContentRetrieveHandler, self).__init__(id)
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
class FileDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, file_id):
        super(FileDeleteHandler, self).__init__(id)
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
class FileSetsRetrieveHandler(ResourceListRetrieveHandler):

    def handle_response(self):
        
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        result = [file_set.to_dict() for file_set in repository.file_sets]
        
        return result, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class FileSetsCreateHandler(ResourceListCreateHandler):

    def handle_response(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        args['repository'] = repository
        
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.create(**args)
        
        return file_set.to_dict(), 201

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('create:file-set')


# ----------------------------------------------------------------------------------------------------------------------
class FileSetRetrieveHandler(ResourceRetrieveHandler):

    def __init__(self, id, file_set_id):
        super(FileSetRetrieveHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):
        
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=self.id())
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(self.file_set_id(), repository.name)
        
        return file_set.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('retrieve:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class FileSetUpdateHandler(ResourceUpdateHandler):

    def __init__(self, id, file_set_id):
        super(FileSetUpdateHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=self.id())
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(self.file_set_id(), repository.name)

        if args['name'] != file_set.name:
            file_set.name = args['name']
        file_set_dao.save(file_set)

        return file_set.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('update:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class FileSetDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, file_set_id):
        super(FileSetDeleteHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=self.id())
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(self.file_set_id(), repository.name)
        
        file_set_dao.delete(file_set)

        return {}, 204

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('delete:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class FileSetFilesRetrieveHandler(ResourceListRetrieveHandler):

    def __init__(self, id, file_set_id):
        super(FileSetFilesRetrieveHandler, self).__init__(id)
        self._file_set_id = file_set_id

    def file_set_id(self):
        return self._file_set_id

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=self.id())
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(self.file_set_id(), repository.name)
        
        result = [f.to_dict() for f in file_set.files]
        
        return result, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class FileSetFileUpdateHandler(ResourceUpdateHandler):

    def __init__(self, id, file_set_id, file_id):
        super(FileSetFileUpdateHandler, self).__init__(id)
        self._file_set_id = file_set_id
        self._file_id = file_id

    def file_set_id(self):
        return self._file_set_id
    
    def file_id(self):
        return self._file_id

    def handle_response(self):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=self.id())
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(self.file_set_id(), repository.name)
        
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=self.file_id())
        if f.repository != repository:
            raise FileNotInRepositoryException(self.file_id(), repository.name)
        
        file_set.add_file(f)
        file_set_dao.save(file_set)
        
        return file_set.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('update:file-set@{}'.format(self.file_set_id()))


# ----------------------------------------------------------------------------------------------------------------------
class FileSetFileDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, file_set_id, file_id):
        super(FileSetFileDeleteHandler, self).__init__(id)
        self._file_set_id = file_set_id
        self._file_id = file_id

    def file_set_id(self):
        return self._file_set_id
    
    def file_id(self):
        return self._file_id

    def handle_response(self):
    
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=self.id())
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=self.id())
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(self.file_set_id(), repository.name)
    
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=self.file_id())
        if f.repository != repository:
            raise FileNotInRepositoryException(self.file_id(), repository.name)
    
        file_set.remove_file(f)
        file_set_dao.save(file_set)
    
        return file_set.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:repository@{}'.format(self.id()))
        self.current_user().check_permission('update:file-set@{}'.format(self.file_set_id()))
