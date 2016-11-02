# ----------------------------------------------------------------------------------------------------------------------
class MissingSettingException(Exception):
    
    def __init__(self, item):
        message = 'Missing item \'{}\' in settings'.format(item)
        super(MissingSettingException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class InvalidSettingException(Exception):
    
    def __init__(self, item, message):
        message = 'Invalid item \'{}\' in settings: {}'.format(item, message)
        super(InvalidSettingException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class ModelNotFoundException(Exception):

    def __init__(self, name, criteria):
        message = 'Model {} with criteria {} not found'.format(name, criteria)
        super(ModelNotFoundException, self).__init__(message)
