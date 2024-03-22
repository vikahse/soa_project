from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config[
    'JWT_SECRET_KEY'] = '3d64e41e753e070ceee4525794d7fab1b2c6f2dc0e38495c04f2fc21c0078eace311fef8c56852dc2e46cb3433cf776c15c6d7dd2b527a4fb0e2b0906363fece'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@db:5433/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

jwt = JWTManager(app)

from backend.app import routes
from backend.app import models

with app.app_context():
    db.create_all()
