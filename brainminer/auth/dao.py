from brainminer.base.dao import BaseDao


# ----------------------------------------------------------------------------------------------------------------------
class UserDao(BaseDao):
    
    def __init__(self, db_session):
        super(UserDao, self).__init__(None, db_session)
