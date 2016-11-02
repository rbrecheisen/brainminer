from brainminer.base.handlers import ResourceListGetHandler, ResourceListPostHandler


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFilesResourceGetHandler(ResourceListGetHandler):
    
    @staticmethod
    def response():
        return [], 200


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFilesResourcePostHandler(ResourceListPostHandler):
    
    @staticmethod
    def response():
        return {}, 201
