import random
import time
from flask import Blueprint, current_app, render_template
from flask_login import login_required
from app.extensions import mqtt, socketio
from app.db import fill_db

bp = Blueprint('communication', __name__)
devices_id_list = ['1', '2']
mqtt_topic = 'my-smart-devices'


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
    return current_app.config['SOMETHING']


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(f"{mqtt_topic}/#")
    print("Connected to MQTT broker")
    # Generate random data messages
    # mqtt.publish(
    #     topic=f"{mqtt_topic}/{random.choice(devices_id_list)}/boiler_temp",
    #     payload=random.randrange(0, 100)
    # )


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = int(message.payload)
    topic = message.topic

    split_topic = topic.split('/')
    parameter_name = split_topic[2]
    controller_id = split_topic[1]

    print(f"controller_id: {controller_id}, parameter_name: {parameter_name}, payload: {payload}")
    # Returns None if not such key
    # controller_id_to_check = users_online_controller_id.get(controller_id)
    # if parameter_name == "boiler_temp" and controller_id_to_check:
    #     print(f'controller_id: {controller_id}, parameter_name: {parameter_name}, payload: {payload}')
    #     print(f'Online controllers: {users_online_controller_id}')
    #
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    # socketio_topic = f'{controller_id_to_check}'
    socketio_topic = "my_topic_hash"
    socketio.emit(socketio_topic, data=data)

    fill_db(topic, payload)

    # Send next MQTT message
    time.sleep(3)
    mqtt.publish(f"{mqtt_topic}/{random.choice(devices_id_list)}/boiler_temp", payload=random.randrange(0, 100))
