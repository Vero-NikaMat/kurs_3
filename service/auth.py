import calendar
import datetime

import jwt
from flask_restx import abort

from constants import JWT_SECRET, JWT_ALGORITHM

class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    def generate_tokens(self, name, password):
        user = self.user_service.get_by_username(name)

        if user is None:
            raise abort(404)

        if not self.user_service.compare_passwords(user.password, password):
            abort(400)

        data = {
            "name": user.name,
            "id": user.id
          }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data,key=JWT_SECRET, algorithm=JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data,key=JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.encode(jwt = refresh_token, key = JWT_SECRET, algorithm=[JWT_ALGORITHM])
        name = data.get("name")

        return self.generate_tokens(name, None)
