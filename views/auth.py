from flask import request
from flask_restx import Resource, Namespace
from service.auth import AuthService

auth_ns = Namespace('auth')

@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        data = request.json
        username = data.get("username", None)
        password = data.get("password", None)

        if None in [username, password]:
            return "", 400

        tokens = AuthService.generate_tokens(username, password)
        return tokens, 201


    def put(self):
        data = request.json
        token = data.get("refresh_token")
        tokens = AuthService.approve_refresh_token(token)

        return tokens, 201