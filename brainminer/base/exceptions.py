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
class ModelFieldValueException(Exception):

    def __init__(self, model, field, value):
        message = 'Model field \'{}\' has invalid value \'{}\''.format(model, field, value)
        super(ModelFieldValueException, self).__init__(message)
