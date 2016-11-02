import os
import json
from flask import Flask, make_response, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from brainminer.base.models import Base
from brainminer.base.api import RootResource
from brainminer.auth.api import (
    TokensResource, UsersResource, UserResource, UserGroupsResource, UserGroupResource,
    UserGroupUsersResource, UserGroupUserResource)
from brainminer.storage.api import (
    RepositoriesResource, RepositoryResource, RepositoryFilesResource, RepositoryFileResource,
    RepositoryFileSetsResource, RepositoryFileSetResource, RepositoryFileSetFilesResource,
    RepositoryFileSetFileResource)

app = Flask(__name__)
app.config.from_pyfile(
    os.getenv('BRAINMINER_SETTINGS', os.path.abspath('brainminer/settings.py')))

api = Api(app)
api.add_resource(RootResource, RootResource.URI)
api.add_resource(TokensResource, TokensResource.URI)
api.add_resource(UsersResource, UsersResource.URI)
api.add_resource(UserResource, UserResource.URI.format('<int:id>'))
api.add_resource(UserGroupsResource, UserGroupsResource.URI)
api.add_resource(UserGroupResource, UserGroupResource.URI.format('<int:id>'))
api.add_resource(UserGroupUsersResource, UserGroupUsersResource.URI.format('<int:id>'))
api.add_resource(UserGroupUserResource, UserGroupUserResource.URI.format('<int:id>', '<int:user_id>'))
api.add_resource(RepositoriesResource, RepositoriesResource.URI)
api.add_resource(RepositoryResource, RepositoryResource.URI.format('<int:id>'))
api.add_resource(RepositoryFilesResource, RepositoryFilesResource.URI.format('<int:id>'))
api.add_resource(RepositoryFileResource, RepositoryFileResource.URI.format('<int:id>', '<int:file_id>'))
api.add_resource(RepositoryFileSetsResource, RepositoryFileSetsResource.URI.format('<int:id>'))
api.add_resource(RepositoryFileSetResource, RepositoryFileSetResource.URI.format('<int:id>', '<int:file_set_id>'))
api.add_resource(RepositoryFileSetFilesResource, RepositoryFileSetFilesResource.URI.format('<int:id>', '<int:file_set_id>'))
api.add_resource(RepositoryFileSetFileResource, RepositoryFileSetFileResource.URI.format('<int:id>', '<int:file_set_id>', '<int:file_id>'))

db = SQLAlchemy(app)


# ----------------------------------------------------------------------------------------------------------------------
@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


# ----------------------------------------------------------------------------------------------------------------------
@app.before_first_request
def init_db(drop=False):
    Base.query = db.session.query_property()
    if drop:
        Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(bind=db.engine)


# ----------------------------------------------------------------------------------------------------------------------
@app.before_request
def before_request():
    g.config = app.config
    g.db_session = db.session


# ----------------------------------------------------------------------------------------------------------------------
@app.teardown_appcontext
def shutdown_database(e):
    db.session.remove()


if __name__ == '__main__':

    host = os.getenv('BRAINMINER_HOST', '0.0.0.0')
    port = os.getenv('BRAINMINER_PORT', '5000')
    port = int(port)

    app.run(host=host, port=port)
