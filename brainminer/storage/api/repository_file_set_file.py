from brainminer.base.api import PermissionProtectedResource
from brainminer.storage.dao import RepositoryDao, FileDao, FileSetDao
from brainminer.storage.exceptions import FileNotInRepositoryException, FileSetNotInRepositoryException


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFilesResource(PermissionProtectedResource):

    URI = '/repositories/{}/file-sets/{}/files'

    def get(self, id, file_set_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve:file-set@{}'.format(file_set_id))

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=file_set_id)
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(file_set.name, repository.name)
        result = []
        if self.has_permission('retrieve:file'):
            result = [f.to_dict() for f in file_set.files]
        else:
            for f in file_set.files:
                if self.has_permission('retrieve:file@{}'.format(f.id)):
                    result.append(f.to_dict())

        return result, 200


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryFileSetFileResource(PermissionProtectedResource):

    URI = '/repositories/{}/file-sets/{}/files/{}'

    def put(self, id, file_set_id, file_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve,update:file-set@{}'.format(file_set_id))

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=file_set_id)
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(file_set.name, repository.name)
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=file_id)
        if f.repository != repository:
            raise FileNotInRepositoryException(f.name, repository.name)
        file_set.add_file(f)
        file_set_dao.save(file_set)

        return file_set.to_dict(), 200

    def delete(self, id, file_set_id, file_id):

        self.check_permission('retrieve:repository@{}'.format(id))
        self.check_permission('retrieve,update:file-set@{}'.format(file_set_id))

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=file_set_id)
        if file_set.repository != repository:
            raise FileSetNotInRepositoryException(file_set.name, repository.name)
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=file_id)
        if f.repository != repository:
            raise FileNotInRepositoryException(f.name, repository.name)
        file_set.remove_file(f)
        file_set_dao.save(file_set)

        return file_set.to_dict(), 200
