from flask_login import UserMixin
from flask_app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    controller_id = db.Column(db.String(100))

    boler_temp = db.relationship('BoilerTemp', backref='user')
    mfb_temp = db.relationship('MfbTemp', backref='user')


class BoilerTemp(db.Model):
    __tablename__ = 'boiler_temp'

    id = db.Column(db.Integer, primary_key=True)
    controller_id = db.Column(db.String(100), db.ForeignKey('users.controller_id'))
    value = db.Column(db.Integer)
    time_stamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False)


class MfbTemp(db.Model):
    __tablename__ = 'mfb_temp'

    id = db.Column(db.Integer, primary_key=True)
    controller_id = db.Column(db.String(100), db.ForeignKey('users.controller_id'))
    value = db.Column(db.Integer)
    time_stamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False)


