import os

# ------------------------------------------------------------------------------------------------------------------
# Flask settings
# ------------------------------------------------------------------------------------------------------------------

BUNDLE_ERRORS = True
PROPAGATE_EXCEPTIONS = True
RESTFUL_JSON = {'indent': 2, 'sort_keys': True}

# ------------------------------------------------------------------------------------------------------------------
# Database settings
# ------------------------------------------------------------------------------------------------------------------

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLITE_DB_FILE = '/tmp/brainminer.db'

if os.getenv('DB_USER', None) is not None:
    SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_USER'),
        os.getenv('DB_PASS'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_NAME'))
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(SQLITE_DB_FILE)
    
DATABASE = SQLALCHEMY_DATABASE_URI.split(':')[0]

# ------------------------------------------------------------------------------------------------------------------
# Upload settings
# ------------------------------------------------------------------------------------------------------------------

UPLOAD_DIR = '/tmp/files'
if not os.path.isdir(UPLOAD_DIR):
    os.system('mkdir -p {}'.format(UPLOAD_DIR))

# ------------------------------------------------------------------------------------------------------------------
# UI settings
# ------------------------------------------------------------------------------------------------------------------

UI_DIR = '/Users/Ralph/development/brainminer/brainminer/ui/static'

# ------------------------------------------------------------------------------------------------------------------
# Security settings
# ------------------------------------------------------------------------------------------------------------------

SECRET_KEY = os.urandom(64)

PASSWORD_SCHEMES = ['pbkdf2_sha512']

USERS = [
    {
        'username': 'root',
        'password': 'secret',
        'email': 'ralph.brecheisen@gmail.com',
        'first_name': 'Ralph',
        'last_name': 'Brecheisen',
        'is_superuser': True,
        'is_admin': True,
        'is_active': True,
        'is_visible': True,
    },
]
