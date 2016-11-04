# ----------------------------------------------------------------------------------------------------------------------
class SecretKeyNotFoundException(Exception):
    
    def __init__(self):
        message = 'Secret key not found in configuration'
        super(SecretKeyNotFoundException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class SecretKeyInvalidException(Exception):
    
    def __init__(self):
        message = 'Secret key invalid'
        super(SecretKeyInvalidException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class MissingAuthorizationHeaderException(Exception):
    
    def __init__(self):
        message = 'Missing authorization header'
        super(MissingAuthorizationHeaderException, self).__init__(message)
        
        
# ----------------------------------------------------------------------------------------------------------------------
class TokenEncodingFailedException(Exception):
    
    def __init__(self, message=None):
        message = 'Failed to encode user info ({})'.format(message)
        super(TokenEncodingFailedException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class TokenDecodingFailedException(Exception):
    
    def __init__(self, message=None):
        message = 'Failed to decode user info from token ({})'.format(message)
        super(TokenDecodingFailedException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class UserNotFoundException(Exception):
    
    def __init__(self, **kwargs):
        message = 'User not found'
        if len(kwargs.keys()) > 0:
            message = 'User \'{}\' not found'.format(kwargs[kwargs.keys()[0]])
        super(UserNotFoundException, self).__init__(message)
    
    
# ----------------------------------------------------------------------------------------------------------------------
class UserNotActiveException(Exception):
    
    def __init__(self, **kwargs):
        message = 'User is not active'
        if len(kwargs.keys()) > 0:
            message = 'User \'{}\' is not active'.format(kwargs[kwargs.keys()[0]])
        super(UserNotActiveException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class InvalidPasswordException(Exception):
    
    def __init__(self):
        message = 'Invalid password'
        super(InvalidPasswordException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class PermissionDeniedException(Exception):
    
    def __init__(self, permission):
        message = 'Permission \'{}\' denied'.format(permission)
        super(PermissionDeniedException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class UserNotSuperUserException(Exception):
    
    def __init__(self, username):
        message = 'User \'{}\' not super user'.format(username)
        super(UserNotSuperUserException, self).__init__(message)
        
        
# ----------------------------------------------------------------------------------------------------------------------
class UserNotAdminException(Exception):
    
    def __init__(self, username):
        message = 'User \'{}\' not admin'.format(username)
        super(UserNotAdminException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class PermissionNotAssignedToUserException(Exception):
    
    def __init__(self, permission, username):
        message = 'Permission \'{}\' not assigned to user \'{}\''.format(permission, username)
        super(PermissionNotAssignedToUserException, self).__init__(message)


# ----------------------------------------------------------------------------------------------------------------------
class PermissionNotAssignedToUserGroupException(Exception):
    def __init__(self, permission, name):
        message = 'Permission \'{}\' not assigned to user group \'{}\''.format(permission, name)
        super(PermissionNotAssignedToUserGroupException, self).__init__(message)
