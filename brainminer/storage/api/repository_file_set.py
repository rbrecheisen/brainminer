from flask_restful import reqparse
from brainminer.base.api import PermissionProtectedResource
from brainminer.storage.dao import RepositoryDao, FileSetDao
from brainminer.storage.exceptions import FileSetNotInRepositoryException


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetsResource(PermissionProtectedResource):

    URI = '/repositories/{}/file-sets'

    def get(self, id):

        self.check_permission('retrieve:repository@{}'.format(id))

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        result = []
        if self.has_permission('retrieve:file-set'):
            result = [file_set.to_dict() for file_set in repository.file_sets]
        else:
            for file_set in repository.file_sets:
                if self.has_permission('retrieve:file-set@{}'.format(file_set.id)):
                    result.append(file_set.to_dict())

        return result, 200

    def post(self, id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('create:file-set')

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        args['repository'] = repository
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.create(**args)

        return file_set.to_dict(), 201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetResource(PermissionProtectedResource):

    URI = '/repositories/{}/file-sets/{}'

    def get(self, id, file_set_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve:file-set@{}'.format(file_set_id))

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=file_set_id)
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(file_set.name, repository.name)

        return file_set.to_dict(), 200

    def put(self, id, file_set_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve,update:file-set@{}'.format(file_set_id))

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=file_set_id)
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(file_set.name, repository.name)
        if args['name'] != file_set.name:
            file_set.name = args['name']
        file_set_dao.save(file_set)

        return file_set.to_dict(), 200

    def delete(self, id, file_set_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve,delete:file-set@{}'.format(file_set_id))

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=file_set_id)
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(file_set.name, repository.name)
        file_set_dao.delete(file_set)

        return {}, 204
