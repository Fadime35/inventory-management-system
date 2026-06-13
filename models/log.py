from models import db

class Log(db.Model):

    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )