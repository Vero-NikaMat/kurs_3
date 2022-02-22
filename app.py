from flask import Flask
from flask_restx import Api
import hashlib

from config import Config
from implemented import user_service
from service.user import UserService
from setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.auth import auth_ns
from views.register import register_ns
from views.user import user_ns
from dao.model.user import User


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.app_context().push()
    register_extensions(app)
    create_data(app, db)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(register_ns)


def create_data(app, db):
    with app.app_context():
        # db.drop_all()
        db.create_all()

        u1 = User(username="vasya", password=UserService(user_service).make_user_password_hash("my_little_pony"), role="user")
        u2 = User(username="oleg", password=UserService(user_service).make_user_password_hash("qwerty"), role="user")
        u3 = User(username="oleg", password=UserService(user_service).make_user_password_hash("P@ssw0rd"), role="admin")

        with db.session.begin():
            db.session.add_all([u1, u2, u3])


if __name__ == '__main__':
    app = create_app(Config())
    app.debug = True
    app.run(host="localhost", port=10001)
