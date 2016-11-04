# ----------------------------------------------------------------------------------------------------------------------
class FileNotInRepositoryException(Exception):

    def __init__(self, file_id, repository_name):
        message = 'File \'{}\' not in repository \'{}\''.format(file_id, repository_name)
        super(FileNotInRepositoryException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class FileSetNotInRepositoryException(Exception):
    
    def __init__(self, file_set_id, repository_name):
        message = 'File set \'{}\' not in repository \'{}\''.format(file_set_id, repository_name)
        super(FileSetNotInRepositoryException, self).__init__(message)
