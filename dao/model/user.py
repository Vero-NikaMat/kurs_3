from marshmallow import Schema, fields
from setup_db import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    favorite_genre = db.Column(db.String(30))
    role = db.Column(db.String(30))


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()
    role = fields.Str()