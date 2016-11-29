from flask import g
from brainminer.base.api import LoginProtectedResource
from brainminer.auth.authentication import create_token


# ----------------------------------------------------------------------------------------------------------------------
class TokensResource(LoginProtectedResource):

    URI = '/tokens'

    @staticmethod
    def post():

        token = create_token(g.current_user)
        
        return {
            'token': token,
            'is_admin': g.current_user.is_admin
        }, 201
