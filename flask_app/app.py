import time

import eventlet
from eventlet import wsgi
import random
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

from init import app, db, login_manager
from models import User, BoilerTemp
from db import fill_db

eventlet.monkey_patch()

# Create db and two example users if not exist
# Use same credentials (email and password) to login
db.create_all()
db.session.commit()

user = User.query.first()
if not user:
    user_1 = User(email="user1@mail.com", controller_id=1, password=generate_password_hash("password", method='sha256'))
    user_2 = User(email="user2@mail.com", controller_id=2, password=generate_password_hash("password", method='sha256'))
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
SUBSCRIBE_MQTT_TOPIC = 'my-smart-devices/#'
PUBLISH_MQTT_TOPIC = 'my-smart-devices'

mqtt = Mqtt(app)
socketio = SocketIO(app)

current_user_controller_id = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Send initial MQTT message
devices_id_list = ['1', '2']
mqtt.publish(topic=f'{PUBLISH_MQTT_TOPIC}/{random.choice(devices_id_list)}/boiler_temp', payload=random.randrange(0, 100), retain=True)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(SUBSCRIBE_MQTT_TOPIC)
    # Generate random data messages

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = int(message.payload)
    topic = message.topic

    split_topic = topic.split('/')
    parameter_name = split_topic[2]
    controller_id = split_topic[1]

    if parameter_name == "boiler_temp" and controller_id == current_user_controller_id:
        print(f'controller_id: {controller_id}, parameter_name: {parameter_name}, payload: {payload}')
        print(f'Current user: {current_user_controller_id}')

        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )
        socketio.emit('mqtt_message', data=data)

        fill_db(topic, payload)

    # Send next MQTT message
    time.sleep(1)
    mqtt.publish(f'{PUBLISH_MQTT_TOPIC}/{random.choice(devices_id_list)}/boiler_temp', payload=random.randrange(0, 100))

@app.route('/')
def index():
    return render_template("index.html")
    # return render_template("data_log.html")

@app.route('/profile')
@login_required
def profile():

    return render_template('profile.html', current_user=current_user)

@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('profile'))

@app.route('/logout')
@login_required
def logout():
    global current_user_controller_id
    current_user_controller_id = None
    logout_user()
    return redirect(url_for('index'))

# Shows real time incoming messages
@app.route('/log')
@login_required
def log():
    global current_user_controller_id
    current_user_controller_id = current_user.controller_id

    return render_template('data_log.html', current_user=current_user)

# Show stored data
@app.route('/data')
@login_required
def data():
    boiler_temp_data = BoilerTemp.query.filter_by(controller_id=current_user.controller_id).all()

    return render_template('stored_data.html', boiler_temp_data=boiler_temp_data)

wsgi.server(eventlet.listen(('', 5000)), app, debug=True)
