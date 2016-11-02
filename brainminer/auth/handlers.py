from flask import g
from brainminer.base.handlers import (
    ResourceListPostHandler, ResourceListGetHandler, ResourceGetHandler, ResourcePutHandler, ResourceDeleteHandler)
from brainminer.auth.authentication import create_token
from brainminer.auth.parameters import UserQueryParameters, UserCreateParameters, UserUpdateParameters
from brainminer.auth.dao import UserDao, UserGroupDao


# ----------------------------------------------------------------------------------------------------------------------
class TokensPostHandler(ResourceListPostHandler):

    def handle_response(self):
        
        token = create_token(g.current_user)
        return {'token': token}, 201

    def check_permissions(self):
        pass


# ----------------------------------------------------------------------------------------------------------------------
class UsersGetHandler(ResourceListGetHandler):
    
    def handle_response(self):

        parameters = UserQueryParameters()
        user_dao = UserDao(self.db_session())
        users = user_dao.retrieve_all(**parameters.get())
        result = [user.to_dict() for user in users]

        return result, 200
    
    def check_permissions(self):
        self.current_user().check_permission('retrieve:user')


# ----------------------------------------------------------------------------------------------------------------------
class UsersPostHandler(ResourceListPostHandler):
    
    def handle_response(self):

        parameters = UserCreateParameters()
        user_dao = UserDao(self.db_session())
        user = user_dao.create(**parameters.get())

        return user.to_dict(), 201
    
    def check_permissions(self):
        self.current_user().check_permission('create:user')
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserGetHandler(ResourceGetHandler):
    
    def handle_response(self):

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())

        return user.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:user@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class UserPutHandler(ResourcePutHandler):
    
    def handle_response(self):

        parameters = UserUpdateParameters()
        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())
        args = parameters.get()

        if args['username'] != user.username:
            user.username = args['username']
        if args['password'] != user.password:
            user.password = args['password']
        if args['email'] != user.email:
            user.email = args['email']
        if args['first_name'] != user.first_name:
            user.first_name = args['first_name']
        if args['last_name'] != user.last_name:
            user.last_name = args['last_name']
        if args['is_admin'] != user.is_admin:
            user.is_admin = args['is_admin']
        if args['is_active'] != user.is_active:
            user.is_active = args['is_active']

        user = user_dao.save(user)

        return user.to_dict(), 200
    
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
