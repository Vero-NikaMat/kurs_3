from flask import request
from flask_restx import Resource, Namespace

from service.auth import AuthService
from setup_db import db

from service.user import UserService
from implemented import user_service
from dao.model.user import User

register_ns = Namespace('register')


@register_ns.route("/")
class RegisterView(Resource):

    def post(self):
        data = request.form
        email = data.get("email", None)
        password = data.get("password", None)
        name = data.get("name", None)
        surname = data.get("surname", None)
        favorite_genre = data.get("favorite_genre", None)

        if None in [name, password]:
            return "", 400


        generate_password = UserService(user_service).make_user_password_hash(password)

        u1 = User(email=email, name=name, password=generate_password, surname=surname, favorite_genre=favorite_genre )
        with db.session.begin():
            db.session.add_all([u1])

        if u1:
            tokens = AuthService(user_service).generate_tokens(name=name, password=password)
            return tokens, 201
        else:
            return "", 400



