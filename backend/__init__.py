import logging
from logging.handlers import SMTPHandler
import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from backend.common.error_handling import ObjectNotFound, AppErrorBaseClass
from backend.common.filters import format_datetime

auth = HTTPBasicAuth()
db = SQLAlchemy()
migrate = Migrate()  # Se crea un objeto de tipo Migrate
cors = CORS()

# Initialize variables
def create_app(settings_module="config.development"):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    # Load the configuration from the instance folder
    if app.config.get("TESTING", False):
        app.config.from_pyfile("config-testing.py", silent=True)
    else:
        app.config.from_pyfile("config.py", silent=True)

    configure_logging(app)
    # Extensions
    db.init_app(app)
    # Se inicializa el objeto migrate
    migrate.init_app(app, db)
    # cors simple usage  
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    #  Registro de los Blueprints

    from .auth import auth_bp

    app.register_blueprint(auth_bp)

    # Registra manejadores de errores personalizados
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({"msg": "Internal server error"}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({"msg": "Method not allowed"}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({"msg": "Forbidden error"}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({"msg": "Not Found error"}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({"msg": str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({"msg": str(e)}), 404


def configure_logging(app):
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]
    
    
    # errors logged to this file
    file_handler = logging.FileHandler('app.log')
    # only log errors and above
    file_handler.setLevel(logging.ERROR)
    # attach the handler to the app's logger
    app.logger.addHandler(file_handler)
    # Añadimos el logger por defecto a la lista de loggers
    loggers = [
        app.logger,
        logging.getLogger("sqlalchemy"),
        logging.getLogger("HTTPAuth"),
        logging.getLogger('flask_cors'),
    ]
    handlers = []
    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    #console_handler.setFormatter(verbose_formatter())

    if (
        (app.config["APP_ENV"] == app.config["APP_ENV_LOCAL"])
        or (app.config["APP_ENV"] == app.config["APP_ENV_TESTING"])
        or (app.config["APP_ENV"] == app.config["APP_ENV_DEVELOPMENT"])
    ):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config["APP_ENV"] == app.config["APP_ENV_PRODUCTION"]:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)
        mail_handler = SMTPHandler(
            (app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            app.config["DONT_REPLY_FROM_EMAIL"],
            app.config["ADMINS"],
            "[Error][{}] La aplicación falló".format(app.config["APP_ENV"]),
            (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"]),
            (),
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)

    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)


def verbose_formatter():
    return logging.Formatter(
        "[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )


def mail_handler_formatter():
    return logging.Formatter(
        """
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d
            Message:
            %(message)s
        """,
        datefmt="%d/%m/%Y %H:%M:%S",
    )

import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    green = '\033[92m'
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%d/%m/%Y %H:%M:%S")
        return formatter.format(record)