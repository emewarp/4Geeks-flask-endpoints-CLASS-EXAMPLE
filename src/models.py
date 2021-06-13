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

    @classmethod
    def get_alarms(cls):
        alarms = cls.query.all()
        return alarms

    @classmethod
    def get_alarm_by_id(cls, id):
        alarm = cls.query.filter_by(id=id).one_or_none()
        return alarm

    @classmethod
    def delete_alarm(cls, id):
        cls.query.filter_by(id=id).delete()
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

