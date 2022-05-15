# config/staging.py
from .default import *
APP_ENV = APP_ENV_STAGING
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'