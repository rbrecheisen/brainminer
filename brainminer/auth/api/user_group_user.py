from brainminer.base.api import PermissionProtectedResource
from brainminer.auth.dao import UserGroupDao, UserDao


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUsersResource(PermissionProtectedResource):

    URI = '/user-groups/{}/users'

    def get(self, id):

        self.check_admin()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        result = [user.to_dict() for user in user_group.users]

        return result, 200


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupUserResource(PermissionProtectedResource):

    URI = '/user-groups/{}/users/{}'

    def put(self, id, user_id):

        self.check_admin()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=user_id)
        user_group.add_user(user)
        user_group_dao.save(user_group)

        return user_group.to_dict(), 200

    def delete(self, id, user_id):

        self.check_admin()

        user_group_dao = UserGroupDao(self.db_session())
        user_group = user_group_dao.retrieve(id=id)
        user_dao = UserDao(self.db_session())
        user = user_dao.retrieve(id=user_id)
        user_group.remove_user(user)
        user_group_dao.save(user_group)

        return user_group.to_dict(), 200
