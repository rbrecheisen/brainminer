from brainminer.base.api import PermissionProtectedResource


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFilesResource(PermissionProtectedResource):

    URI = '/repositories/{}/file-sets/{}/files'

    def get(self, id, file_set_id):
        return [], 200


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFileResource(PermissionProtectedResource):

    URI = '/repositories/{}/file-sets/{}/files/{}'

    def put(self, id, file_set_id, file_id):
        return {}, 200

    def delete(self, id, file_set_id, file_id):
        return {}, 200
