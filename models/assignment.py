from models import db

class Assignment(db.Model):

    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))

    assigned_date = db.Column(db.Date)
    status = db.Column(db.String(20))

    # RELATIONSHIPS (JOIN için)
    product = db.relationship("Product", backref="assignments")
    employee = db.relationship("Employee", backref="assignments")