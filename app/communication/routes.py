import random
import time

from flask import Blueprint, current_app, render_template
from flask_login import login_required, current_user
from app.extensions import mqtt, socketio
# from app.utils import fill_db
from app.models import fill_db2
from app.extensions import controller_id_to_hash

bp = Blueprint('communication', __name__)
devices_id_list = ['1', '2']
mqtt_topic = 'my-smart-devices'

mqtt_to_socketio_topic = "my_topic"


@bp.route('/mqtt_client')
@login_required
def mqtt_client():
    return render_template('mqtt_client.html')


@bp.route('/mqtt-init')
def index():
    global mqtt_topic
    mqtt_topic = current_app.config['MQTT_TOPIC']
    print(current_app.config['MQTT_TOPIC'])
    mqtt.publish(
        topic=f"{current_app.config['MQTT_TOPIC']}/{random.choice(devices_id_list)}/boiler_temp",
        payload=random.randrange(0, 100)
    )
    return current_app.config['MQTT_TOPIC']


@socketio.on(mqtt_to_socketio_topic)
def handle_socketio_message(message):
    payload = int(message.payload)
    topic = message.topic

    print(f'Current user {current_user}')
    print(f'Topic: {topic}, Payload : {payload}')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(f"{mqtt_topic}/#")
    print("Connected to MQTT broker")
    # Send random MQTT messages to initialize the loop
    mqtt.publish(
        topic=f"{mqtt_topic}/{random.choice(devices_id_list)}/boiler_temp",
        payload=random.randrange(0, 100)
    )


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):

    payload = int(message.payload)
    topic = message.topic

    split_topic = topic.split('/')
    parameter_name = split_topic[2]
    controller_id = split_topic[1]

    # print(f"controller_id: {controller_id}, parameter_name: {parameter_name}, payload: {payload}")
    # Returns None if not such key
    controller_id_hash = controller_id_to_hash.get(controller_id)
    if parameter_name == "boiler_temp" and controller_id_hash:
    # if parameter_name == "boiler_temp" and current_user.id:
        print(f'controller_id: {controller_id}, parameter_name: {parameter_name}, payload: {payload}')
        print(f'Online controllers: {controller_id_to_hash}')

        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )

        socketio_topic = f'{controller_id_hash}'
        socketio.emit(socketio_topic, data=data)

    fill_db2(topic, payload, mqtt.app)

    # Send next MQTT message
    time.sleep(3)
    mqtt.publish(f"{mqtt_topic}/{random.choice(devices_id_list)}/boiler_temp", payload=random.randrange(0, 100))
