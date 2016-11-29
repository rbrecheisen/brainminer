import os
import json
from flask import Flask, make_response, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from brainminer.base.models import Base
from brainminer.base.exceptions import MissingSettingException, InvalidSettingException
from brainminer.auth.api.token import TokensResource
from brainminer.auth.api.user import UsersResource, UserResource
from brainminer.auth.api.user_group import UserGroupsResource, UserGroupResource
from brainminer.auth.api.user_group_user import UserGroupUsersResource, UserGroupUserResource
from brainminer.auth.api.user_permission import UserPermissionsResource, UserPermissionResource
from brainminer.auth.api.user_group_permission import UserGroupPermissionsResource, UserGroupPermissionResource
from brainminer.storage.api.repository import RepositoriesResource, RepositoryResource
from brainminer.storage.api.repository_file import (
    RepositoryFilesResource, RepositoryFileResource, RepositoryFileContentResource)
from brainminer.storage.api.repository_file_set import RepositoryFileSetsResource, RepositoryFileSetResource
from brainminer.storage.api.repository_file_set_file import RepositoryFileSetFilesResource, RepositoryFileSetFileResource
from brainminer.auth.dao import UserDao, UserGroupDao

# Specify 'ui' folder as static content folder but set its URL path to '/'
app = Flask(__name__, static_url_path='', static_folder='ui')
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
api.add_resource(TokensResource, TokensResource.URI)
api.add_resource(UsersResource, UsersResource.URI)
api.add_resource(UserResource, UserResource.URI.format('<int:id>'))
api.add_resource(UserPermissionsResource, UserPermissionsResource.URI.format('<int:id>'))
api.add_resource(UserPermissionResource, UserPermissionResource.URI.format('<int:id>', '<int:permission_id>'))
api.add_resource(UserGroupsResource, UserGroupsResource.URI)
api.add_resource(UserGroupResource, UserGroupResource.URI.format('<int:id>'))
api.add_resource(UserGroupPermissionsResource, UserGroupPermissionsResource.URI.format('<int:id>'))
api.add_resource(UserGroupPermissionResource, UserGroupPermissionResource.URI.format('<int:id>', '<int:permission_id>'))
api.add_resource(UserGroupUsersResource, UserGroupUsersResource.URI.format('<int:id>'))
api.add_resource(UserGroupUserResource, UserGroupUserResource.URI.format('<int:id>', '<int:user_id>'))
api.add_resource(RepositoriesResource, RepositoriesResource.URI)
api.add_resource(RepositoryResource, RepositoryResource.URI.format('<int:id>'))
api.add_resource(RepositoryFilesResource, RepositoryFilesResource.URI.format('<int:id>'))
api.add_resource(RepositoryFileResource, RepositoryFileResource.URI.format('<int:id>', '<int:file_id>'))
api.add_resource(RepositoryFileContentResource, RepositoryFileContentResource.URI.format('<int:id>', '<int:file_id>'))
api.add_resource(RepositoryFileSetsResource, RepositoryFileSetsResource.URI.format('<int:id>'))
api.add_resource(RepositoryFileSetResource, RepositoryFileSetResource.URI.format('<int:id>', '<int:file_set_id>'))
api.add_resource(RepositoryFileSetFilesResource, RepositoryFileSetFilesResource.URI.format('<int:id>', '<int:file_set_id>'))
api.add_resource(RepositoryFileSetFileResource, RepositoryFileSetFileResource.URI.format('<int:id>', '<int:file_set_id>', '<int:file_id>'))

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
    if isinstance(data, dict) or isinstance(data, list):
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

    # If we're using SQLite (instead of PostgreSQL) remove database file
    if app.config['DATABASE'] == 'sqlite':
        os.system('rm -f {}'.format(app.config['SQLITE_DB_FILE']))
        
    # This code gets executed only if we're doing local testing, so remove the /tmp/files
    # folder where all uploaded files gets stored.
    os.system('rm -f {}/*'.format(app.config['UPLOAD_DIR']))
    
    # Set host and port number for local testing
    host = os.getenv('BRAINMINER_HOST', '0.0.0.0')
    port = os.getenv('BRAINMINER_PORT', '5000')
    port = int(port)

    # Run application
    print(' * Click here for UI: http://0.0.0.0:5000/index.html')
    app.run(host=host, port=port)
