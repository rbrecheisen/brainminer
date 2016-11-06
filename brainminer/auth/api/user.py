from flask_restful import reqparse
from brainminer.base.api import PermissionProtectedResource
from brainminer.auth.dao import UserDao


# ----------------------------------------------------------------------------------------------------------------------
class UsersResource(PermissionProtectedResource):

    URI = '/users'

    def get(self):

        self.check_admin()

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='args')
        parser.add_argument('email', type=str, location='args')
        parser.add_argument('first_name', type=str, location='args')
        parser.add_argument('last_name', type=str, location='args')
        parser.add_argument('is_admin', type=bool, location='args')
        parser.add_argument('is_active', type=bool, location='args')
        args = parser.parse_args()

        user_dao = UserDao(self.db_session())
        result = [user.to_dict() for user in user_dao.retrieve_all(**args)]

        return result, 200

    def post(self):

        self.check_admin()

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


# ----------------------------------------------------------------------------------------------------------------------
class UserResource(PermissionProtectedResource):

    URI = '/users/{}'

    def get(self, id):

        self.check_admin()

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=id)

        return user.to_dict(), 200

    def put(self, id):

        self.check_permission('update:user@{}'.format(id))

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
        user = user_dao.retrieve(id=id)

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

    def delete(self, id):

        self.check_admin()

        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=id)
        user_dao.delete(user)

        return {}, 204
