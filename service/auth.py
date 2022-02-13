import calendar
import datetime

import jwt
from flask_restx import abort

from constants import JWT_SECRET, JWT_ALGORITHM

class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    def generate_tokens(self, username, password):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        if not self.user_service.compare_passwords(user.pasword, password):
            abort(400)

        data = {
            "username": user.username,
            "role": user.role
          }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


    def approve_refresh_token(self, refresh_token):
        data = jwt.encode(jwt = refresh_token, key = JWT_SECRET, algorithm=[JWT_ALGORITHM])
        username = data.get("username")

        return self.generate_tokens(username, None, is_refresh = True)
