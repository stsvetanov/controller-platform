from flask_login import UserMixin
from flask import current_app
import sqlite3
from datetime import datetime
import logging
from app.extensions import db


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


def fill_db2(topic, payload, app):
    split_topic = topic.split('/')
    parameter_name = split_topic[2]
    controller_id = split_topic[1]
    boiler_temp = BoilerTemp(controller_id=controller_id, value=payload, time_stamp=datetime.now())
    with app.app_context():
        db.session.add(boiler_temp)
        db.session.commit()


# def fill_db(path, parameter):
#     conn = None
#     time_stamp = datetime.now()
#     try:
#         conn = sqlite3.connect('web_app.db')
#         cur = conn.cursor()
#         split_topic = path.split('/')
#         parameter_name = split_topic[2]
#         controller_id = split_topic[1]
#
#         sql_query = f'INSERT INTO {parameter_name}(value , time_stamp, controller_id) VALUES (?,?,?)'
#         cur.execute(sql_query, [parameter, time_stamp, controller_id])
#     except Exception:
#         conn.rollback()
#         logging.error("Database connection error")
#         raise
#     else:
#         conn.commit()
#     finally:
#         cur.close()

