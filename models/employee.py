from models import db

class Employee(db.Model):

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    department = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    email = db.Column(db.String(120))