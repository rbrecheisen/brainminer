from flask_restful import reqparse
from brainminer.base.api import PermissionProtectedResource
from brainminer.storage.dao import RepositoryDao


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesResource(PermissionProtectedResource):

    URI = '/repositories'

    def get(self):

        self.check_permission('retrieve:repository')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()
        repository_dao = RepositoryDao(self.db_session())
        result = [repository.to_dict() for repository in repository_dao.retrieve_all(**args)]

        return result, 200

    def post(self):

        self.check_permission('create:repository')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.create(**args)

        return repository.to_dict(), 201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryResource(PermissionProtectedResource):

    URI = '/repositories/{}'

    def get(self, id):

        self.check_permission('retrieve:repository@{}'.format(id))
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)

        return repository.to_dict(), 200

    def put(self, id):

        self.check_permission('retrieve,update:repository@{}'.format(id))
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        if args['name'] != repository.name:
            repository.name = args['name']
        repository_dao.save(repository)

        return repository.to_dict(), 200

    def delete(self, id):

        self.check_permission('retrieve,delete:repository@{}'.format(id))
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        repository_dao.delete(repository)

        return {}, 204
