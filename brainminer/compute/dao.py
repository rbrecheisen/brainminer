from brainminer.base.dao import BaseDao
from brainminer.compute.models import Classifier, Session


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierDao(BaseDao):
    def __init__(self, db_session):
        super(ClassifierDao, self).__init__(Classifier, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class SessionDao(BaseDao):
    def __init__(self, db_session):
        super(SessionDao, self).__init__(Session, db_session)
