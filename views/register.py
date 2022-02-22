from flask import request
from flask_restx import Resource, Namespace

from setup_db import db

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

        from service.user import UserService
        from implemented import user_service
        generate_password = UserService(user_service).make_user_password_hash(password)

        from dao.model.user import User
        u1 = User(email=email, name=name, password=generate_password, surname=surname, favorite_genre=favorite_genre )
        with db.session.begin():
            db.session.add_all([u1])

        return "user create", 200
