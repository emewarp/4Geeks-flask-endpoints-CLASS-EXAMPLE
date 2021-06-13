from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alarm(db.Model):
    __tablename__ = 'alarm'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120))
    priority = db.Column(db.String(80))
    ack = db.Column(db.Boolean())

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "priority": self.priority,
            "ack": self.ack,
        }

    def create(self):
        db.session.add(self)
        db.session.commit()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

