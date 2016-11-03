from flask import g
from flask_restful import reqparse
from brainminer.base.handlers import (
    ResourceListCreateHandler, ResourceListRetrieveHandler, ResourceRetrieveHandler, ResourceUpdateHandler, ResourceDeleteHandler)
from brainminer.auth.authentication import create_token
from brainminer.auth.dao import UserDao, UserGroupDao


# ----------------------------------------------------------------------------------------------------------------------
class TokensCreateHandler(ResourceListCreateHandler):

    def handle_response(self):
        
        token = create_token(g.current_user)
        return {'token': token}, 201

    def check_permissions(self):
        pass


# ----------------------------------------------------------------------------------------------------------------------
class UsersRetrieveHandler(ResourceListRetrieveHandler):
    
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
class UsersCreateHandler(ResourceListCreateHandler):
    
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
class UserRetrieveHandler(ResourceRetrieveHandler):
    
    def handle_response(self):

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())

        return user.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:user@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class UserUpdateHandler(ResourceUpdateHandler):
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('first_name', type=str, location='json')
        parser.add_argument('last_name', type=str, location='json')
        parser.add_argument('is_admin', type=bool, location='json')
        parser.add_argument('is_active', type=bool, location='json')
        args = parser.parse_args()

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())

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

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())
        user_dao.delete(user)

        return {}, 204
    
    def check_permissions(self):
        self.current_user().check_permission('delete:user@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupsRetrieveHandler(ResourceListRetrieveHandler):
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()

        user_group_dao = UserGroupDao(self.db_session())
        user_groups = user_group_dao.retrieve_all(**args)
        result = [user_group.to_dict() for user_group in user_groups]

        return result, 200
    
    def check_permissions(self):
        self.current_user().check_permission('retrieve:user-group')
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupsCreateHandler(ResourceListCreateHandler):
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.create(**args)

        return user_group.to_dict(), 201

    def check_permissions(self):
        self.current_user().check_permission('create:user-group')

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupRetrieveHandler(ResourceRetrieveHandler):
    
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())

        return user_group.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:user-group@{}'.format(self.id()))

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUpdateHandler(ResourceUpdateHandler):
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())

        if args['name'] != user_group.name:
            user_group.name = args['name']

        user_group_dao.save(user_group)

        return user_group.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('update:user-group@{}'.format(self.id()))

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupDeleteHandler(ResourceDeleteHandler):
    
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        user_group_dao.delete(user_group)

        return {}, 204

    def check_permissions(self):
        self.current_user().check_permission('delete:user-group@{}'.format(self.id()))


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUsersRetrieveHandler(ResourceListRetrieveHandler):
    
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        result = [user.to_dict() for user in user_group.users]

        return result, 200

    def check_permissions(self):
        self.current_user().check_permission('retrieve:user-group@{}'.format(self.id()))

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUserUpdateHandler(ResourceUpdateHandler):
    
    def __init__(self, id, user_id):
        super(UserGroupUserUpdateHandler, self).__init__(id)
        self._user_id = user_id
        
    def user_id(self):
        return self._user_id
        
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.user_id())
        user_group.add_user(user)
        user_group_dao.save(user_group)

        return user_group.to_dict(), 200

    def check_permissions(self):
        # First check whether we're allowed to retrieve the user we're trying to add
        self.current_user().check_permission('retrieve:user@{}'.format(self.user_id()))
        # Then check whether we're allowed to update the user group
        self.current_user().check_permission('update:user-group@{}'.format(self.id()))

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUserDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, user_id):
        super(UserGroupUserDeleteHandler, self).__init__(id)
        self._user_id = user_id

    def user_id(self):
        return self._user_id

    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.user_id())
        user_group.remove_user(user)
        user_group_dao.save(user_group)

        return user_group.to_dict(), 200

    def check_permissions(self):
        self.current_user().check_permission('update:user-group@{}'.format(self.id()))
