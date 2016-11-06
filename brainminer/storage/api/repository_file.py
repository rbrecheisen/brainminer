from brainminer.base.api import PermissionProtectedResource


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFilesResource(PermissionProtectedResource):

    URI = '/repositories/{}/files'

    def get(self, id):
        return [], 200

    def post(self, id):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileResource(PermissionProtectedResource):

    URI = '/repositories/{}/files/{}'

    def get(self, id, file_id):
        return {}, 200

    def delete(self, id, file_id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileContentResource(PermissionProtectedResource):

    URI = '/repositories/{}/files/{}/content'

    def get(self, id, file_id):
        return {}, 200
