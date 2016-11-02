from brainminer.base.api import LoginProtectedResource, TokenProtectedResource


# ----------------------------------------------------------------------------------------------------------------------
class TokensResource(LoginProtectedResource):
    
    URI = '/tokens'
    
    def post(self):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class UsersResource(TokenProtectedResource):

    URI = '/users'
    
    def get(self):
        return [], 200
    
    def post(self):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class UserResource(TokenProtectedResource):

    URI = '/users/{}'
    
    def get(self, id):
        return {}, 200
    
    def put(self, id):
        return {}, 200
    
    def delete(self, id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupsResource(TokenProtectedResource):

    URI = '/user-groups'
    
    def get(self):
        return [], 200
    
    def post(self):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupResource(TokenProtectedResource):

    URI = '/user-groups/{}'

    def get(self, id):
        return {}, 200

    def put(self, id):
        return {}, 200

    def delete(self, id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUsersResource(TokenProtectedResource):

    URI = '/user-groups/{}/users'
    
    def get(self, id):
        return [], 200


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUserResource(TokenProtectedResource):

    URI = '/user-groups/{}/users/{}'
    
    def put(self, id, user_id):
        return {}, 200
    
    def delete(self, id, user_id):
        return {}, 200
