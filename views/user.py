from flask import request, abort

from helpers.decorators import auth_required

from flask_restx import Resource, Namespace
from dao.model.user import UserSchema
from implemented import user_service
from service.auth import AuthService
from service.user import UserService
from setup_db import db

user_ns = Namespace('users')

@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200


    def post(self):
        req_json = request.json
        user = user_service.create(req_json)

        return {"location": f"/users/{user.id}"}, 201


@user_ns.route('/<int:uid>')
class UserView(Resource):

    @auth_required
    def get(self, uid):
        r = user_service.get_one(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def patch(self, uid):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        if not req_json.get('id'):
            req_json['id'] = uid
        return UserService(db.session).update(req_json)


    def put(self, uid, password1, password2):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user = UserService(db.session).get_one(uid)
        if user.password == password1:
            user.password = UserService(user_service).make_user_password_hash(password2)
            user_service.update(user)
            tokens = AuthService(user_service).generate_tokens(name=user.name, password=password2)
            return tokens, 201
        else:
            return "", 400