import os

# ------------------------------------------------------------------------------------------------------------------
# Flask settings
# ------------------------------------------------------------------------------------------------------------------

PROPAGATE_EXCEPTIONS = True
RESTFUL_JSON = {'indent': 2, 'sort_keys': True}

# ------------------------------------------------------------------------------------------------------------------
# Database settings
# ------------------------------------------------------------------------------------------------------------------

SQLALCHEMY_TRACK_MODIFICATIONS = False

if os.getenv('DB_USER', None) is not None:
    SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_USER'),
        os.getenv('DB_PASS'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_NAME'))
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/brainminer.db'
