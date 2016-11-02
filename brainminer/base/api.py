from flask_restful import Resource
from brainminer.auth.exceptions import (
    MissingAuthorizationHeaderException, UserNotFoundException, UserNotActiveException, InvalidPasswordException,
    SecretKeyNotFoundException, SecretKeyInvalidException, TokenDecodingFailedException)
from brainminer.auth.authentication import check_login, check_token


# ----------------------------------------------------------------------------------------------------------------------
class BaseResource(Resource):

    def dispatch_request(self, *args, **kwargs):
        # We can some additional logging or checking here...
        return super(BaseResource, self).dispatch_request(*args, **kwargs)


# ----------------------------------------------------------------------------------------------------------------------
class RootResource(BaseResource):
    
    URI = '/'
    
    def get(self):
        return {'message': 'Welcome to BrainMiner'}, 200
    
    
# ----------------------------------------------------------------------------------------------------------------------
class LoginProtectedResource(BaseResource):

    def dispatch_request(self, *args, **kwargs):
        
        message = None
        
        try:
            check_login()
        except MissingAuthorizationHeaderException as e:
            message = e.message
        except UserNotFoundException as e:
            message = e.message
        except UserNotActiveException as e:
            message = e.message
        except InvalidPasswordException as e:
            message = e.message
            
        if message is not None:
            print('[ERROR] LoginProtectedResource.dispatch_request() {}'.format(message))
            return {'message': message}, 403
        
        return super(BaseResource, self).dispatch_request(*args, **kwargs)


# ----------------------------------------------------------------------------------------------------------------------
class TokenProtectedResource(BaseResource):

    def dispatch_request(self, *args, **kwargs):
        
        message = None
        
        try:
            check_token()
        except MissingAuthorizationHeaderException as e:
            message = e.message
        except SecretKeyNotFoundException as e:
            message = e.message
        except SecretKeyInvalidException as e:
            message = e.message
        except TokenDecodingFailedException as e:
            message = e.message
        except UserNotFoundException as e:
            message = e.message
        except UserNotActiveException as e:
            message = e.message
            
        if message is not None:
            print('[ERROR] TokenProtectedResource.dispatch_request() {}'.format(message))
            return {'message': message}, 403
        
        return super(BaseResource, self).dispatch_request(*args, **kwargs)
