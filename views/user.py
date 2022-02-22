from flask import request

from helpers.decorators import auth_required

from flask_restx import Resource, Namespace
from dao.model.user import UserSchema
from implemented import user_service


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
    def get(self, rid):
        r = user_service.get_one(rid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def patch(self, rid):
        pass

    def put(self, rid):
        pass