# config/testing.py
from .default import *
# Parámetros para activar el modo debug
TESTING = True
DEBUG = True
APP_ENV = APP_ENV_TESTING
SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'