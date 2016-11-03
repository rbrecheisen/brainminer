import os
import json
from flask import Flask, make_response, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from brainminer.base.models import Base
from brainminer.base.exceptions import MissingSettingException, InvalidSettingException
from brainminer.base.api import RootResource
from brainminer.auth.api import (
    TokensResource, UsersResource, UserResource, UserGroupsResource, UserGroupResource,
    UserGroupUsersResource, UserGroupUserResource)
from brainminer.storage.api import (
    RepositoriesResource, RepositoryResource, FilesResource, FileResource,
    FileContentResource, FileSetsResource, FileSetResource,
    FileSetFilesResource, FileSetFileResource)
from brainminer.auth.dao import UserDao, UserGroupDao

app = Flask(__name__)
app.config.from_pyfile(
    os.getenv('BRAINMINER_SETTINGS', os.path.abspath('brainminer/settings.py')))

if 'SQLITE_DB_FILE' not in app.config.keys():
    raise MissingSettingException('SQLITE_DB_FILE')
if 'SQLALCHEMY_DATABASE_URI' not in app.config.keys():
    raise MissingSettingException('SQLALCHEMY_DATABASE_URI')
if 'DATABASE' not in app.config.keys():
    raise MissingSettingException('DATABASE')
if 'SECRET_KEY' not in app.config.keys():
    raise MissingSettingException('SECRET_KEY')
if 'PASSWORD_SCHEMES' not in app.config.keys():
    raise MissingSettingException('PASSWORD_SCHEMES')
if 'USERS' not in app.config.keys():
    raise MissingSettingException('USERS')
if 'UPLOAD_DIR' not in app.config.keys():
    raise MissingSettingException('UPLOAD_DIR')

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
api.add_resource(FilesResource, FilesResource.URI.format('<int:id>'))
api.add_resource(FileResource, FileResource.URI.format('<int:id>', '<int:file_id>'))
api.add_resource(FileContentResource, FileContentResource.URI.format('<int:id>', '<int:file_id>'))
api.add_resource(FileSetsResource, FileSetsResource.URI.format('<int:id>'))
api.add_resource(FileSetResource, FileSetResource.URI.format('<int:id>', '<int:file_set_id>'))
api.add_resource(FileSetFilesResource, FileSetFilesResource.URI.format('<int:id>', '<int:file_set_id>'))
api.add_resource(FileSetFileResource, FileSetFileResource.URI.format('<int:id>', '<int:file_set_id>', '<int:file_id>'))

db = SQLAlchemy(app)


# ----------------------------------------------------------------------------------------------------------------------
def init_tables():
    # Check there is a 'root' user in the settings. The username should be
    # 'root' and the 'is_superuser' should be True.
    found = False
    for item in app.config['USERS']:
        if item['username'] == 'root':
            if not item['is_superuser']:
                raise InvalidSettingException('USERS', 'User \'root\' not super user')
            found = True
            break
    if not found:
        raise InvalidSettingException('USERS', 'User \'root\' missing')
    # Check there is only 1 super user in the settings
    count = 0
    for item in app.config['USERS']:
        if item['is_superuser']:
            count += 1
    if count != 1:
        raise InvalidSettingException('USERS', 'More than 1 super user ({})'.format(count))
    # Create users
    user_dao = UserDao(db.session)
    for item in app.config['USERS']:
        user = user_dao.retrieve(username=item['username'])
        if user is None:
            user_dao.create(
                username=item['username'],
                password=item['password'],
                email=item['email'],
                first_name=item['first_name'],
                last_name=item['last_name'],
                is_superuser=item['is_superuser'],
                is_admin=item['is_admin'],
                is_active=item['is_active'],
                is_visible=item['is_visible'])
    # Create user groups if these have been defined in the settings (optional)
    if 'USER_GROUPS' in app.config.keys():
        user_group_dao = UserGroupDao(db.session)
        for item in app.config['USER_GROUPS']:
            user_group = user_group_dao.retrieve(name=item['name'])
            if user_group is None:
                user_group_dao.create(name=item['name'])


# ----------------------------------------------------------------------------------------------------------------------
def drop_tables():
    Base.metadata.drop_all(db.engine)
    
    
# ----------------------------------------------------------------------------------------------------------------------
@api.representation('application/json')
def output_json(data, code, headers=None):
    if isinstance(data, dict):
        # Only wrap data in JSON string if it's a dictionary. If it's a file
        # stream we directly return it
        response = make_response(json.dumps(data), code)
        response.headers.extend(headers or {})
        return response
    return data


# ----------------------------------------------------------------------------------------------------------------------
@app.before_first_request
def init_db(drop=False):
    Base.query = db.session.query_property()
    if drop:
        drop_tables()
    Base.metadata.create_all(bind=db.engine)
    init_tables()


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

    if app.config['DATABASE'] == 'sqlite':
        os.system('rm -f {}'.format(app.config['SQLITE_DB_FILE']))
    
    host = os.getenv('BRAINMINER_HOST', '0.0.0.0')
    port = os.getenv('BRAINMINER_PORT', '5000')
    port = int(port)

    app.run(host=host, port=port)
