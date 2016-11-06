from brainminer.base.api import PermissionProtectedResource


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesResource(PermissionProtectedResource):

    URI = '/repositories'

    def get(self):
        return [], 200

    def post(self):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryResource(PermissionProtectedResource):

    URI = '/repositories/{}'

    def get(self, id):
        return {}, 200

    def put(self, id):
        return {}, 200

    def delete(self, id):
        return {}, 204
