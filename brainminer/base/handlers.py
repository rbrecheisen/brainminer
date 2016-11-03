from flask import g
from flask_restful import HTTPException
from brainminer.auth.exceptions import PermissionDeniedException


# ----------------------------------------------------------------------------------------------------------------------
class ResourceHandler(object):
    
    def __init__(self, id=None):
        self._id = id
        
    def id(self):
        return self._id
    
    def response(self):

        try:
            self.check_permissions()
        except PermissionDeniedException as e:
            print('[ERROR] {}.check_permissions() {}'.format(self.__class__.__name__, e.message))
            return {'message': e.message}, 403

        try:
            return self.handle_response()
        except HTTPException as e:
            print('[ERROR] {}.handle_response() {}'.format(self.__class__.__name__, e.data))
            return e.data, e.code
        except Exception as e:
            print('[ERROR] {}.handle_response() {}'.format(self.__class__.__name__, e.message))
            return {'message': e.message}, 400

    def check_permissions(self):
        raise NotImplementedError()
    
    def handle_response(self):
        raise NotImplementedError()

    @staticmethod
    def db_session():
        return g.db_session

    @staticmethod
    def current_user():
        return g.current_user

    @staticmethod
    def config():
        return g.config


# ----------------------------------------------------------------------------------------------------------------------
class ResourceGetHandler(ResourceHandler):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class ResourcePutHandler(ResourceHandler):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class ResourceDeleteHandler(ResourceHandler):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class ResourceListHandler(ResourceHandler):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class ResourceListGetHandler(ResourceListHandler):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class ResourceListPostHandler(ResourceListHandler):
    pass
