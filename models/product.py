from models import db

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(100))

    brand = db.Column(db.String(100))

    model = db.Column(db.String(100))

    serial_no = db.Column(db.String(100), unique=True)

    stock = db.Column(db.Integer, default=0)