from flask_restful import reqparse
from brainminer.base.api import PermissionProtectedResource
from brainminer.auth.dao import UserGroupDao, PermissionDao
from brainminer.auth.exceptions import PermissionNotAssignedToUserGroupException


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionsResource(PermissionProtectedResource):

    URI = '/user-groups/{}/permissions'

    def get(self, id):

        self.check_admin()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        result = [p.to_dict() for p in user_group.permissions]

        return result, 200

    def post(self, id):

        self.check_admin()

        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, required=True, location='json')
        parser.add_argument('resource_class', type=str, required=True, location='json')
        parser.add_argument('resource_id', type=int, location='json')
        parser.add_argument('granted', type=bool, location='json')
        args = parser.parse_args()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        args['principal'] = user_group
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.create(**args)

        return permission.to_dict(), 201


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupPermissionResource(PermissionProtectedResource):

    URI = '/user-groups/{}/permissions/{}'

    def get(self, id, permission_id):

        self.check_admin()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=permission_id)
        if permission.principal != user_group:
            raise PermissionNotAssignedToUserGroupException(permission.to_str(), user_group.name)

        return permission.to_dict(), 200

    def put(self, id, permission_id):

        self.check_admin()

        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, location='json')
        parser.add_argument('resource_class', type=str, location='json')
        parser.add_argument('resource_id', type=int, location='json')
        parser.add_argument('granted', type=bool, location='json')
        args = parser.parse_args()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=permission_id)
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

    def delete(self, id, permission_id):

        self.check_admin()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        permission_dao = PermissionDao(self.db_session())
        permission = permission_dao.retrieve(id=permission_id)
        if permission.principal != user_group:
            raise PermissionNotAssignedToUserGroupException(permission.to_str(), user_group.name)
        permission_dao.delete(permission_dao)

        return {}, 204
