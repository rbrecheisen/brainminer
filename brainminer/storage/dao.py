from brainminer.base.dao import BaseDao
from brainminer.storage.models import Repository, File, FileSet


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryDao(BaseDao):

    def __init__(self, db_session):
        super(RepositoryDao, self).__init__(Repository, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class FileDao(BaseDao):

    def __init__(self, db_session):
        super(FileDao, self).__init__(File, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class FileSetDao(BaseDao):

    def __init__(self, db_session):
        super(FileSetDao, self).__init__(FileSet, db_session)
