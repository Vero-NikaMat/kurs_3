from flask import request
from flask_restx import Resource, Namespace

from setup_db import db

register_ns = Namespace('register')


@register_ns.route("/")
class RegisterView(Resource):

    def post(self):
        data = request.form
        username = data.get("username", None)
        password = data.get("password", None)

        if None in [username, password]:
            return "", 400

        from service.user import UserService
        from implemented import user_service
        passwd = UserService(user_service).make_user_password_hash("my_little_pony")

        from dao.model.user import User
        u1 = User(username=username, password=UserService(user_service).make_user_password_hash(password), role="user")
        with db.session.begin():
            db.session.add_all([u1])

        return "user create", 200
