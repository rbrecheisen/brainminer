from brainminer.base.api import LoginProtectedResource, TokenProtectedResource
from brainminer.auth.handlers import (
    TokensPostHandler, UsersGetHandler, UsersPostHandler, UserGetHandler, UserPutHandler, UserDeleteHandler,
    UserGroupsGetHandler, UserGroupsPostHandler, UserGroupGetHandler, UserGroupPutHandler, UserGroupDeleteHandler,
    UserGroupUsersGetHandler, UserGroupUserPutHandler, UserGroupUserDeleteHandler)


# ----------------------------------------------------------------------------------------------------------------------
class TokensResource(LoginProtectedResource):
    
    URI = '/tokens'
    
    @staticmethod
    def post():
        handler = TokensPostHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UsersResource(TokenProtectedResource):

    URI = '/users'
    
    @staticmethod
    def get():
        handler = UsersGetHandler()
        return handler.response()
    
    @staticmethod
    def post():
        handler = UsersPostHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserResource(TokenProtectedResource):

    URI = '/users/{}'
    
    @staticmethod
    def get(id):
        handler = UserGetHandler(id)
        return handler.response()
    
    @staticmethod
    def put(id):
        handler = UserPutHandler(id)
        return handler.response()
    
    @staticmethod
    def delete(id):
        handler = UserDeleteHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupsResource(TokenProtectedResource):

    URI = '/user-groups'
    
    @staticmethod
    def get():
        handler = UserGroupsGetHandler()
        return handler.response()
    
    @staticmethod
    def post():
        handler = UserGroupsPostHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupResource(TokenProtectedResource):

    URI = '/user-groups/{}'

    @staticmethod
    def get(id):
        handler = UserGroupGetHandler(id)
        return handler.response()

    @staticmethod
    def put(id):
        handler = UserGroupPutHandler(id)
        return handler.response()

    @staticmethod
    def delete(id):
        handler = UserGroupDeleteHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUsersResource(TokenProtectedResource):

    URI = '/user-groups/{}/users'
    
    @staticmethod
    def get(id):
        handler = UserGroupUsersGetHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUserResource(TokenProtectedResource):

    URI = '/user-groups/{}/users/{}'
    
    @staticmethod
    def put(id, user_id):
        handler = UserGroupUserPutHandler(id, user_id)
        return handler.response()
    
    @staticmethod
    def delete(id, user_id):
        handler = UserGroupUserDeleteHandler(id, user_id)
        return handler.response()
