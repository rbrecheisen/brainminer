from brainminer.base.api import TokenProtectedResource
from brainminer.storage.handlers import (
    RepositoriesRetrieveHandler, RepositoriesCreateHandler, RepositoryRetrieveHandler, RepositoryUpdateHandler,
    RepositoryDeleteHandler, FilesRetrieveHandler, FilesCreateHandler, FileRetrieveHandler,
    FileContentRetrieveHandler, FileDeleteHandler, FileSetsRetrieveHandler)


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesResource(TokenProtectedResource):

    URI = '/repositories'
    
    def get(self):
        handler = RepositoriesRetrieveHandler()
        return handler.response()
    
    def post(self):
        handler = RepositoriesCreateHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryResource(TokenProtectedResource):

    URI = '/repositories/{}'
    
    def get(self, id):
        handler = RepositoryRetrieveHandler()
        return handler.response()
    
    def put(self, id):
        handler = RepositoryUpdateHandler()
        return handler.response()
    
    def delete(self, id):
        handler = RepositoryDeleteHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class FilesResource(TokenProtectedResource):

    URI = '/repositories/{}/files'
    
    def get(self, id):
        handler = FilesRetrieveHandler(id)
        return handler.response()
    
    def post(self, id):
        handler = FilesCreateHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class FileResource(TokenProtectedResource):

    URI = '/repositories/{}/files/{}'
    
    def get(self, id, file_id):
        handler = FileRetrieveHandler(id, file_id)
        return handler.response()
    
    def delete(self, id, file_id):
        handler = FileDeleteHandler(id, file_id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class FileContentResource(TokenProtectedResource):

    URI = '/repositories/{}/files/{}/content'

    def get(self, id, file_id):
        handler = FileContentRetrieveHandler(id, file_id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class FileSetsResource(TokenProtectedResource):

    URI = '/repositories/{}/file-sets'

    def get(self):

        return [], 200
    
    def post(self):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class FileSetResource(TokenProtectedResource):

    URI = '/repositories/{}/file-sets/{}'
    
    def get(self, id, file_set_id):
        return {}, 200
    
    def put(self, id, file_set_id):
        return {}, 200
    
    def delete(self, id, file_set_id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class FileSetFilesResource(TokenProtectedResource):

    URI = '/repositories/{}/file-sets/{}/files'
    
    def get(self, id, file_set_id):
        return [], 200


# ----------------------------------------------------------------------------------------------------------------------
class FileSetFileResource(TokenProtectedResource):

    URI = '/repositories/{}/file-sets/{}/files/{}'
    
    def put(self, id, file_set_id, file_id):
        return {}, 200
    
    def delete(self, id, file_set_id, file_id):
        return {}, 200
