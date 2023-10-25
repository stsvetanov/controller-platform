from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

db = SQLAlchemy()
login_manager = LoginManager()
mqtt = Mqtt()
socketio = SocketIO()


