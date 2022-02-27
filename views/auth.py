from flask import request, abort
from flask_restx import Resource, Namespace

from implemented import user_service
from service.auth import AuthService
from service.user import UserService
from setup_db import db

auth_ns = Namespace('auth')


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        data = request.form
        email = data.get("email", None)
        password = data.get("password", None)

        if None in [email, password]:
            return "", 400

        user = UserService(db.session).get_by_email(email=email)
        if user.password == password:
            tokens = AuthService(user_service).generate_tokens(name=user.name, password=password)
            return tokens, 201
        else:
            return "", 400


    def put(self):
        data = request.json
        token = data.get("refresh_token")
        tokens = AuthService.approve_refresh_token(token)

        return tokens, 201