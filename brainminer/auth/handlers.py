from flask import g
from flask_restful import reqparse
from brainminer.base.handlers import (
    ResourceListPostHandler, ResourceListGetHandler, ResourceGetHandler, ResourcePutHandler, ResourceDeleteHandler)
from brainminer.auth.authentication import create_token
from brainminer.auth.exceptions import (
    SecretKeyNotFoundException, SecretKeyInvalidException, TokenEncodingFailedException)
from brainminer.auth.dao import UserDao, UserGroupDao


# ----------------------------------------------------------------------------------------------------------------------
class TokensPostHandler(ResourceListPostHandler):

    def handle_response(self):
        
        try:
            token = create_token(g.current_user)
            return {'token': token}, 201
        except SecretKeyNotFoundException as e:
            message = e.message
        except SecretKeyInvalidException as e:
            message = e.message
        except TokenEncodingFailedException as e:
            message = e.message

        print('[ERROR] TokensPostHandler.response() {}'.format(message))
        return {'message': message}, 403


# ----------------------------------------------------------------------------------------------------------------------
class UsersGetHandler(ResourceListGetHandler):
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='args')
        parser.add_argument('email', type=str, location='args')
        parser.add_argument('first_name', type=str, location='args')
        parser.add_argument('last_name', type=str, location='args')
        parser.add_argument('is_admin', type=bool, location='args')
        parser.add_argument('is_active', type=bool, location='args')
        args = parser.parse_args()

        user_dao = UserDao(self.db_session())
        users = user_dao.retrieve_all(**args)
        result = [user.to_dict() for user in users]
        
        return result, 200
    
    def check_permissions(self):
        self.current_user().check_permission('retrieve:user')


# ----------------------------------------------------------------------------------------------------------------------
class UsersPostHandler(ResourceListPostHandler):
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        parser.add_argument('email', type=str, required=True, location='json')
        parser.add_argument('first_name', type=str, location='json')
        parser.add_argument('last_name', type=str, location='json')
        parser.add_argument('is_admin', type=bool, location='json')
        parser.add_argument('is_active', type=bool, location='json')
        args = parser.parse_args()

        user_dao = UserDao(self.db_session())
        user = user_dao.create(**args)

        return user.to_dict(), 201
    
    def check_permissions(self):
        self.current_user().check_permission('create:user')
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserGetHandler(ResourceGetHandler):
    
    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:user@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class UserPutHandler(ResourcePutHandler):
    
    def handle_response(self):
        return {}, 200
    
    def check_permissions(self):
        self.current_user().check_permission('update:user@{}'.format(self.id()))
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserDeleteHandler(ResourceDeleteHandler):
    
    def handle_response(self):
        return {}, 204
    
    def check_permissions(self):
        self.current_user().check_permission('delete:user@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupsGetHandler(ResourceListGetHandler):
    
    def handle_response(self):
        return [], 200
    
    def check_permissions(self):
        self.current_user().check_permission('retrieve:user-group')
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupsPostHandler(ResourceListPostHandler):
    
    def handle_response(self):
        return {}, 201

    def check_permissions(self):
        self.current_user().check_permission('create:user-group')

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupGetHandler(ResourceGetHandler):
    
    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:user-group@{}'.format(self.id()))

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPutHandler(ResourcePutHandler):
    
    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('update:user-group@{}'.format(self.id()))

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupDeleteHandler(ResourceDeleteHandler):
    
    def handle_response(self):
        return {}, 204

    def check_permissions(self):
        self.current_user().check_permission('delete:user-group@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUsersGetHandler(ResourceListGetHandler):
    
    def handle_response(self):
        return [], 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:user-group@{}'.format(self.id()))

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUserPutHandler(ResourcePutHandler):
    
    def __init__(self, id, user_id):
        super(UserGroupUserPutHandler, self).__init__(id)
        self.user_id = user_id
        
    def user_id(self):
        return self.user_id
        
    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        # First check whether we're allowed to retrieve the user we're trying to add
        self.current_user().check_permission('retrieve:user@{}'.format(self.user_id()))
        # Then check whether we're allowed to update the user group
        self.current_user().check_permission('update:user-group@{}'.format(self.id()))

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUserDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, user_id):
        super(UserGroupUserDeleteHandler, self).__init__(id)
        self.user_id = user_id

    def user_id(self):
        return self.user_id

    def handle_response(self):
        return {}, 200

    def check_permissions(self):
        self.current_user().check_permission('update:user-group@{}'.format(self.id()))
