from brainminer.base.api import PermissionProtectedResource


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetsResource(PermissionProtectedResource):

    URI = '/repositories/{}/file-sets'

    def get(self):
        return [], 200

    def post(self):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetResource(PermissionProtectedResource):

    URI = '/repositories/{}/file-sets/{}'

    def get(self, id, file_set_id):
        return {}, 200

    def put(self, id, file_set_id):
        return {}, 200

    def delete(self, id, file_set_id):
        return {}, 204
