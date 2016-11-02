from brainminer.base.api import TokenProtectedResource
from brainminer.storage.handlers import RepositoryFilesResourceGetHandler, RepositoryFilesResourcePostHandler


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesResource(TokenProtectedResource):

    URI = '/repositories'
    
    def get(self):
        return [], 200
    
    def post(self):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryResource(TokenProtectedResource):

    URI = '/repositories/{}'
    
    def get(self, id):
        return {}, 200
    
    def put(self, id):
        return {}, 200
    
    def delete(self, id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFilesResource(TokenProtectedResource):

    URI = '/repositories/{}/files'
    
    def get(self):
        handler = RepositoryFilesResourceGetHandler()
        return handler.response()
    
    def post(self):
        handler = RepositoryFilesResourcePostHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileResource(TokenProtectedResource):

    URI = '/repositories/{}/files/{}'
    
    def get(self, id, file_id):
        return {}, 200
    
    def put(self, id, file_id):
        return {}, 200
    
    def delete(self, id, file_id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetsResource(TokenProtectedResource):

    URI = '/repositories/{}/file-sets'

    def get(self):
        return [], 200
    
    def post(self):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetResource(TokenProtectedResource):

    URI = '/repositories/{}/file-sets/{}'
    
    def get(self, id, file_set_id):
        return {}, 200
    
    def put(self, id, file_set_id):
        return {}, 200
    
    def delete(self, id, file_set_id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFilesResource(TokenProtectedResource):

    URI = '/repositories/{}/file-sets/{}/files'
    
    def get(self, id, file_set_id):
        return [], 200


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFileResource(TokenProtectedResource):

    URI = '/repositories/{}/file-sets/{}/files/{}'
    
    def put(self, id, file_set_id, file_id):
        return {}, 200
    
    def delete(self, id, file_set_id, file_id):
        return {}, 200
