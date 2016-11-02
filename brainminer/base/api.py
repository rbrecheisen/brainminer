from flask import g
from flask_restful import Resource
from brainminer.auth.exceptions import (
    MissingAuthorizationHeaderException, UserNotFoundException, UserNotActiveException, InvalidPasswordException,
    SecretKeyNotFoundException, SecretKeyInvalidException, TokenDecodingFailedException)
from brainminer.auth.authentication import check_login, check_token


# ----------------------------------------------------------------------------------------------------------------------
class BaseResource(Resource):

    def dispatch_request(self, *args, **kwargs):
        # We can some additional logging here...
        return super(BaseResource, self).dispatch_request(*args, **kwargs)

    @staticmethod
    def db_session():
        return g.db_session
    
    @staticmethod
    def current_user():
        return g.current_user
    
    @staticmethod
    def config():
        return g.config


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
            return {'message': message}
        
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
            return {'message': message}
        
        return super(BaseResource, self).dispatch_request(*args, **kwargs)
