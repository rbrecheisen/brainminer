from flask_restful import reqparse
from brainminer.base.api import PermissionProtectedResource
from brainminer.auth.dao import UserGroupDao


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupsResource(PermissionProtectedResource):

    URI = '/user-groups'

    def get(self):

        self.check_admin()

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()

        user_group_dao = UserGroupDao(self.db_session())
        result = [user_group.to_dict() for user_group in user_group_dao.retrieve_all(**args)]

        return result, 200

    def post(self):

        self.check_admin()

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.create(**args)

        return user_group.to_dict(), 201


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupResource(PermissionProtectedResource):

    URI = '/user-groups/{}'

    def get(self, id):

        self.check_admin()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)

        return user_group.to_dict(), 200

    def put(self, id):

        self.check_admin()

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        if args['name'] != user_group.name:
            user_group.name = args['name']
        user_group_dao.save(user_group)

        return user_group.to_dict(), 200

    def delete(self, id):

        self.check_admin()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        user_group_dao.delete(user_group)

        return {}, 204
