# ----------------------------------------------------------------------------------------------------------------------
class ResourceHandler(object):
    
    @staticmethod
    def response():
        return {}, 200


# ----------------------------------------------------------------------------------------------------------------------
class ResourceGetHandler(ResourceHandler):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class ResourcePutHandler(ResourceHandler):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class ResourceDeleteHandler(ResourceHandler):
    
    @staticmethod
    def response():
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class ResourceListHandler(object):
    
    @staticmethod
    def response():
        return [], 200


# ----------------------------------------------------------------------------------------------------------------------
class ResourceListGetHandler(ResourceListHandler):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class ResourceListPostHandler(ResourceListHandler):

    @staticmethod
    def response():
        return {}, 201
