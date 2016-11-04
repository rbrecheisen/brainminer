from flask import g
from flask_restful import reqparse
from brainminer.base.handlers import (
    ResourceListCreateHandler, ResourceListRetrieveHandler, ResourceRetrieveHandler, ResourceUpdateHandler,
    ResourceDeleteHandler)
from brainminer.auth.authentication import create_token
from brainminer.auth.permissions import check_admin
from brainminer.auth.exceptions import PermissionNotAssignedToUserException, PermissionNotAssignedToUserGroupException
from brainminer.auth.dao import UserDao, UserGroupDao, PermissionDao


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
        check_admin(self.current_user())


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
        check_admin(self.current_user())
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserRetrieveHandler(ResourceRetrieveHandler):
    
    def handle_response(self):

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())

        return user.to_dict(), 200

    def check_permissions(self):
        check_admin(self.current_user())


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
        check_admin(self.current_user())
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserDeleteHandler(ResourceDeleteHandler):
    
    def handle_response(self):

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())
        user_dao.delete(user)

        return {}, 204
    
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserPermissionsRetrieveHandler(ResourceListRetrieveHandler):
    
    def handle_response(self):
        
        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())
        result = [p.to_dict() for p in user.permissions]
                    
        return result, 200
        
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserPermissionsCreateHandler(ResourceListCreateHandler):

    def handle_response(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, required=True, location='json')
        parser.add_argument('resource_class', type=str, required=True, location='json')
        parser.add_argument('resource_id', type=int, location='json')
        parser.add_argument('granted', type=bool, location='json')
        args = parser.parse_args()
        
        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())
        args['principal'] = user
        
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.create(**args)

        return permission.to_dict(), 201
    
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserPermissionRetrieveHandler(ResourceRetrieveHandler):
    
    def __init__(self, id, permission_id):
        super(UserPermissionRetrieveHandler, self).__init__(id)
        self._permission_id = permission_id
        
    def permission_id(self):
        return self._permission_id
    
    def handle_response(self):

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=self.permission_id())
        if permission.principal != user:
            raise PermissionNotAssignedToUserException(permission.to_str(), user.username)

        return permission.to_dict(), 200
    
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserPermissionUpdateHandler(ResourceUpdateHandler):

    def __init__(self, id, permission_id):
        super(UserPermissionUpdateHandler, self).__init__(id)
        self._permission_id = permission_id
    
    def permission_id(self):
        return self._permission_id
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, location='json')
        parser.add_argument('resource_class', type=str, location='json')
        parser.add_argument('resource_id', type=int, location='json')
        parser.add_argument('granted', type=bool, location='json')
        args = parser.parse_args()

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=self.permission_id())
        if permission.principal != user:
            raise PermissionNotAssignedToUserException(permission.to_str(), user.username)
        
        if args['action'] != permission.action:
            permission.action = args['action']
        if args['resource_class'] != permission.resource_class:
            permission.resource_class = args['resource_class']
        if args['resource_id'] != permission.resource_id:
            permission.resource_id = args['resource_id']
        if args['granted'] != permission.granted:
            permission.granted = args['granted']
            
        permission_dao.save(permission)

        return permission.to_dict(), 200
    
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserPermissionDeleteHandler(ResourceDeleteHandler):

    def __init__(self, id, permission_id):
        super(UserPermissionDeleteHandler, self).__init__(id)
        self._permission_id = permission_id
    
    def permission_id(self):
        return self._permission_id
    
    def handle_response(self):

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=self.id())
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=self.permission_id())
        if permission.principal != user:
            raise PermissionNotAssignedToUserException(permission.to_str(), user.username)
        
        permission_dao.delete(permission)

        return {}, 204
    
    def check_permissions(self):
        check_admin(self.current_user())


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
        check_admin(self.current_user())
    
    
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
        check_admin(self.current_user())

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupRetrieveHandler(ResourceRetrieveHandler):
    
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())

        return user_group.to_dict(), 200

    def check_permissions(self):
        check_admin(self.current_user())

    
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
        check_admin(self.current_user())

    
# ----------------------------------------------------------------------------------------------------------------------
class UserGroupDeleteHandler(ResourceDeleteHandler):
    
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        user_group_dao.delete(user_group)

        return {}, 204

    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUsersRetrieveHandler(ResourceListRetrieveHandler):
    
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        result = [user.to_dict() for user in user_group.users]

        return result, 200

    def check_permissions(self):
        check_admin(self.current_user())

    
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
        check_admin(self.current_user())


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
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionsRetrieveHandler(ResourceListRetrieveHandler):

    def handle_response(self):
        
        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        result = [p.to_dict() for p in user_group.permissions]
        
        return result, 200
    
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionsCreateHandler(ResourceListCreateHandler):
    
    def handle_response(self):

        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, required=True, location='json')
        parser.add_argument('resource_class', type=str, required=True, location='json')
        parser.add_argument('resource_id', type=int, location='json')
        parser.add_argument('granted', type=bool, location='json')
        args = parser.parse_args()
    
        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        args['principal'] = user_group
    
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.create(**args)
    
        return permission.to_dict(), 201
    
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionRetrieveHandler(ResourceRetrieveHandler):
    
    def __init__(self, id, permission_id):
        super(UserGroupPermissionRetrieveHandler, self).__init__(id)
        self._permission_id = permission_id
    
    def permission_id(self):
        return self._permission_id
    
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=self.permission_id())
        if permission.principal != user_group:
            raise PermissionNotAssignedToUserGroupException(permission.to_str(), user_group.name)

        return permission.to_dict(), 200
    
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionUpdateHandler(ResourceUpdateHandler):
    
    def __init__(self, id, permission_id):
        super(UserGroupPermissionUpdateHandler, self).__init__(id)
        self._permission_id = permission_id
    
    def permission_id(self):
        return self._permission_id
    
    def handle_response(self):
    
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, location='json')
        parser.add_argument('resource_class', type=str, location='json')
        parser.add_argument('resource_id', type=int, location='json')
        parser.add_argument('granted', type=bool, location='json')
        args = parser.parse_args()
    
        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=self.permission_id())
        if permission.principal != user_group:
            raise PermissionNotAssignedToUserGroupException(permission.to_str(), user_group.name)
    
        if args['action'] != permission.action:
            permission.action = args['action']
        if args['resource_class'] != permission.resource_class:
            permission.resource_class = args['resource_class']
        if args['resource_id'] != permission.resource_id:
            permission.resource_id = args['resource_id']
        if args['granted'] != permission.granted:
            permission.granted = args['granted']
    
        permission_dao.save(permission)

        return permission.to_dict(), 200
    
    def check_permissions(self):
        check_admin(self.current_user())


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionDeleteHandler(ResourceDeleteHandler):
    
    def __init__(self, id, permission_id):
        super(UserGroupPermissionDeleteHandler, self).__init__(id)
        self._permission_id = permission_id
    
    def permission_id(self):
        return self._permission_id
    
    def handle_response(self):

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=self.id())
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=self.permission_id())
        if permission.principal != user_group:
            raise PermissionNotAssignedToUserGroupException(permission.to_str(), user_group.name)
        
        permission_dao.delete(permission_dao)
        
        return {}, 204
    
    def check_permissions(self):
        check_admin(self.current_user())
