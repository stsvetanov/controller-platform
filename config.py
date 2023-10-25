import os
from secret import secret_key
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Data base configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'web_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MQTT configuration
    MQTT_BROKER_URL = 'broker.hivemq.com'
    MQTT_BROKER_PORT = 1883
    MQTT_TOPIC = 'my-smart-devices'

    # Session configuration
    SECRET_KEY = secret_key
