from models import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="personel")