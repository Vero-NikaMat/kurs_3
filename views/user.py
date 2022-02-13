from flask import request

from helpers.decorators import admin_required
from setup_db import db


from flask_restx import Resource, Namespace
from dao.model.user import UserSchema
from implemented import user_service



user_ns = Namespace('users')

@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200


    def post(self):
        req_json = request.json
        user = user_service.create(req_json)

        return "", 201, {"location": f"/users/{user.id}"}

@user_ns.route('/<int:uid>')
class UserView(Resource):
    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204


    def get(self, rid):
        r = db.session.query(User).get(rid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200
