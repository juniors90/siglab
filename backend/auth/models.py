import os

from backend import db
from werkzeug.security import generate_password_hash, check_password_hash

import time
import jwt

secret = os.getenv("SECRET_KEY")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        payload = {"id": self.id, "exp": time.time() + expires_in}
        key = secret
        token = jwt.encode(payload=payload, key=key, algorithm="HS256")
        return token.encode("UTF-8")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, secret, algorithms=["HS256"])
        except:
            return
        return User.query.get(data["id"])

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all():
        return User.query.all()
