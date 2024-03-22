from passlib.apps import custom_app_context as pwd_context
from backend.app import db
from flask_jwt_extended import create_access_token


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def get_token(self):
        return create_access_token(identity=self.id)
