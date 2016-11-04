from brainminer.base.api import LoginProtectedResource, TokenProtectedResource
from brainminer.auth.handlers import (
    TokensCreateHandler, UsersRetrieveHandler, UsersCreateHandler, UserRetrieveHandler, UserUpdateHandler,
    UserDeleteHandler, UserGroupsRetrieveHandler, UserGroupsCreateHandler, UserGroupRetrieveHandler,
    UserGroupUpdateHandler, UserGroupDeleteHandler, UserGroupUsersRetrieveHandler, UserGroupUserUpdateHandler,
    UserGroupUserDeleteHandler, UserPermissionsRetrieveHandler, UserPermissionsCreateHandler,
    UserPermissionRetrieveHandler, UserPermissionUpdateHandler, UserPermissionDeleteHandler,
    UserGroupPermissionsRetrieveHandler, UserGroupPermissionsCreateHandler, UserGroupPermissionRetrieveHandler,
    UserGroupPermissionUpdateHandler, UserGroupPermissionDeleteHandler)


# ----------------------------------------------------------------------------------------------------------------------
class TokensResource(LoginProtectedResource):
    
    URI = '/tokens'
    
    @staticmethod
    def post():
        handler = TokensCreateHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UsersResource(TokenProtectedResource):

    URI = '/users'
    
    @staticmethod
    def get():
        handler = UsersRetrieveHandler()
        return handler.response()
    
    @staticmethod
    def post():
        handler = UsersCreateHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserResource(TokenProtectedResource):

    URI = '/users/{}'
    
    @staticmethod
    def get(id):
        handler = UserRetrieveHandler(id)
        return handler.response()
    
    @staticmethod
    def put(id):
        handler = UserUpdateHandler(id)
        return handler.response()
    
    @staticmethod
    def delete(id):
        handler = UserDeleteHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserPermissionsResource(TokenProtectedResource):
    
    URI = '/users/{}/permissions'
    
    @staticmethod
    def get(id):
        handler = UserPermissionsRetrieveHandler(id)
        return handler.response()
    
    @staticmethod
    def post(id):
        handler = UserPermissionsCreateHandler(id)
        return handler.response()
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserPermissionResource(TokenProtectedResource):
    
    URI = '/users/{}/permissions/{}'
    
    @staticmethod
    def get(id, permission_id):
        handler = UserPermissionRetrieveHandler(id, permission_id)
        return handler.response()
    
    @staticmethod
    def put(id, permission_id):
        handler = UserPermissionUpdateHandler(id, permission_id)
        return handler.response()
    
    @staticmethod
    def delete(id, permission_id):
        handler = UserPermissionDeleteHandler(id, permission_id)
        return handler.response()
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupsResource(TokenProtectedResource):

    URI = '/user-groups'
    
    @staticmethod
    def get():
        handler = UserGroupsRetrieveHandler()
        return handler.response()
    
    @staticmethod
    def post():
        handler = UserGroupsCreateHandler()
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupResource(TokenProtectedResource):

    URI = '/user-groups/{}'

    @staticmethod
    def get(id):
        handler = UserGroupRetrieveHandler(id)
        return handler.response()

    @staticmethod
    def put(id):
        handler = UserGroupUpdateHandler(id)
        return handler.response()

    @staticmethod
    def delete(id):
        handler = UserGroupDeleteHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionsResource(TokenProtectedResource):
    
    URI = '/user-groups/{}/permissions'
    
    @staticmethod
    def get(id):
        handler = UserGroupPermissionsRetrieveHandler(id)
        return handler.response()
    
    @staticmethod
    def post(id):
        handler = UserGroupPermissionsCreateHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionResource(TokenProtectedResource):
    
    URI = '/user-groups/{}/permissions/{}'
    
    @staticmethod
    def get(id, permission_id):
        handler = UserGroupPermissionRetrieveHandler(id, permission_id)
        return handler.response()
    
    @staticmethod
    def put(id, permission_id):
        handler = UserGroupPermissionUpdateHandler(id, permission_id)
        return handler.response()
    
    @staticmethod
    def delete(id, permission_id):
        handler = UserGroupPermissionDeleteHandler(id, permission_id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUsersResource(TokenProtectedResource):

    URI = '/user-groups/{}/users'
    
    @staticmethod
    def get(id):
        handler = UserGroupUsersRetrieveHandler(id)
        return handler.response()


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUserResource(TokenProtectedResource):

    URI = '/user-groups/{}/users/{}'
    
    @staticmethod
    def put(id, user_id):
        handler = UserGroupUserUpdateHandler(id, user_id)
        return handler.response()
    
    @staticmethod
    def delete(id, user_id):
        handler = UserGroupUserDeleteHandler(id, user_id)
        return handler.response()
