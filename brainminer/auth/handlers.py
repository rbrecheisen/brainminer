from flask import g
from brainminer.base.handlers import ResourceListPostHandler


# ----------------------------------------------------------------------------------------------------------------------
class TokensResourcePostHandler(ResourceListPostHandler):

    @staticmethod
    def response():
        if g.current_user is None:
            return {'message': 'User is not logged in'}, 403
        return {'token': '1234'}, 201
