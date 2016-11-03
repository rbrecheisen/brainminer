class FileNotInRepositoryException(Exception):

    def __init__(self, file_id, repo_name):
        message = 'File {} not in repository {}'.format(file_id, repo_name)
        super(FileNotInRepositoryException, self).__init__(message)
