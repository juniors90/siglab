# config/dev.py
from .default import *
APP_ENV = APP_ENV_DEVELOPMENT
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'