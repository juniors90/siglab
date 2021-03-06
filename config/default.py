import os

# Define the application directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('SECRET_KEY')
# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# Para propagar las excepciones y poder manejarlas
# a nivel de aplicación.

PROPAGATE_EXCEPTIONS = True

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

# Config email
MAIL_SERVER = 'your_server_smtp'
MAIL_PORT = 587
MAIL_USERNAME = 'your_email_adress'
MAIL_PASSWORD = 'your_password'
DONT_REPLY_FROM_EMAIL = 'from'
ADMINS = ('your_alias@xyz.com', )
MAIL_USE_TLS = True
MAIL_DEBUG = False