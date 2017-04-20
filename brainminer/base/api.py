from flask import g, Response
from flask_restful import Resource, HTTPException, abort
from brainminer.auth.exceptions import (
    MissingAuthorizationHeaderException, UserNotFoundException, UserNotActiveException, InvalidPasswordException,
    SecretKeyNotFoundException, SecretKeyInvalidException, TokenDecodingFailedException, PermissionDeniedException,
    UserNotSuperUserException, UserNotAdminException)
from brainminer.auth.authentication import check_login, check_token
from brainminer.auth.permissions import has_permission, check_permission, check_admin, check_superuser


# ----------------------------------------------------------------------------------------------------------------------
class BaseResource(Resource):

    def dispatch_request(self, *args, **kwargs):

        code = 400

        try:
            return super(BaseResource, self).dispatch_request(*args, **kwargs)
        except HTTPException as e:
            message = e.data['message']
            code = e.code
        except Exception as e:
            message = e.message

        if message is not None:
            print('[ERROR] {}.dispatch_request() {}'.format(self.__class__.__name__, message))
            abort(code, message=message)

    @staticmethod
    def config():
        return g.config

    @staticmethod
    def db_session():
        return g.db_session

    @staticmethod
    def current_user():
        return g.current_user


# ----------------------------------------------------------------------------------------------------------------------
class HtmlResource(BaseResource):

    @staticmethod
    def output_html(data, code, headers=None):
        resp = Response(data, mimetype='text/html', headers=headers)
        resp.status_code = code
        return resp


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
            abort(403, message=message)
        
        return super(LoginProtectedResource, self).dispatch_request(*args, **kwargs)


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
            abort(403, message=message)
        
        return super(TokenProtectedResource, self).dispatch_request(*args, **kwargs)


# ----------------------------------------------------------------------------------------------------------------------
class PermissionProtectedResource(TokenProtectedResource):

    def check_admin(self):

        try:
            check_superuser(self.current_user())
        except UserNotSuperUserException:
            try:
                check_admin(self.current_user())
            except UserNotAdminException as e:
                print('[ERROR] {}.check_permission() {}'.format(self.__class__.__name__, e.message))
                abort(403, message=e.message)

    def check_permission(self, permission):

        try:
            check_permission(self.current_user(), permission)
        except PermissionDeniedException as e:
            print('[ERROR] {}.check_permission() {}'.format(self.__class__.__name__, e.message))
            abort(403, message=e.message)

    def has_permission(self, permission):
        return has_permission(self.current_user(), permission)
