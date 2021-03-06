import logging
import os
import time
from flask import abort, request, jsonify, g, url_for, current_app
import jwt
from flask_cors import cross_origin

from .models import User
from . import auth_bp
from backend import auth, db

logger = logging.getLogger(__name__)


@auth.verify_password
def verify_password(username_or_token, password):
    logger.info("first try token.")
    # first try token
    user = User.verify_auth_token(username_or_token)
    # then check for username and password pair
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth_bp.route("/api/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    # Comprobamos que no hay ya un usuario con ese email
    user = User.get_by_email(email)
    if user is not None:
        error = f"El email {email} ya está siendo utilizado por otro usuario"
        response = jsonify({"msg": error})
        response.status_code = 400
        return response
    # Check for blank requests
    if username is None or password is None:
        abort(400)
    # Check for existing users
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username, email=email)
    user.hash_password(password)
    user.save()
    return (jsonify({"username": user.username, "email": user.email}), 201)


@auth_bp.route("/api/login")
@auth.login_required
def get_token():
    token = g.user.generate_auth_token(600)
    return jsonify({"token": token.decode("utf-8"), "duration": 600})


movies = [
    {
        "name": "The Shawshank Redemption",
        "casts": [
            "Tim Robbins",
            "Morgan Freeman",
            "Bob Gunton",
            "William Sadler",
        ],
        "genres": ["Drama"],
    },
    {
        "name": "The Godfather ",
        "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
        "genres": ["Crime", "Drama"],
    },
]

@cross_origin
@auth_bp.route("/api/movies", methods=["GET"])
#@auth.login_required
def hello():
    current_app.logger.info("Show movies of blog")
    return jsonify(movies)


@auth_bp.route("/api/dothis", methods=["GET"])
@auth.login_required
def do_this():
    return jsonify({"message": "It is done {}".format(g.user.username)})
