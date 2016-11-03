from brainminer.base.api import TokenProtectedResource
from brainminer.storage.handlers import (
    RepositoriesGetHandler, RepositoriesPostHandler, RepositoryGetHandler, RepositoryPutHandler,
    RepositoryDeleteHandler, RepositoryFilesGetHandler, RepositoryFilesPostHandler, RepositoryFileGetHandler,
    RepositoryFileContentGetHandler, RepositoryFileDeleteHandler, RepositoryFileSetsGetHandler)


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesResource(TokenProtectedResource):

    URI = '/repositories'
    
    def get(self):
        handler = RepositoriesGetHandler()
        return handler.response()
    
    def post(self):
        handler = RepositoriesPostHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryResource(TokenProtectedResource):

    URI = '/repositories/{}'
    
    def get(self, id):
        handler = RepositoryGetHandler()
        return handler.response()
    
    def put(self, id):
        handler = RepositoryPutHandler()
        return handler.response()
    
    def delete(self, id):
        handler = RepositoryDeleteHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFilesResource(TokenProtectedResource):

    URI = '/repositories/{}/files'
    
    def get(self, id):
        handler = RepositoryFilesGetHandler(id)
        return handler.response()
    
    def post(self, id):
        handler = RepositoryFilesPostHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileResource(TokenProtectedResource):

    URI = '/repositories/{}/files/{}'
    
    def get(self, id, file_id):
        handler = RepositoryFileGetHandler(id, file_id)
        return handler.response()
    
    def delete(self, id, file_id):
        handler = RepositoryFileDeleteHandler(id, file_id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileContentResource(TokenProtectedResource):

    URI = '/repositories/{}/files/{}/content'

    def get(self, id, file_id):
        handler = RepositoryFileContentGetHandler(id, file_id)
        return handler.response()


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
