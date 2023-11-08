import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

eventlet.monkey_patch()

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'

mqtt_topic = 'my-smart-devices'
mqtt_to_socketio_topic = "my_topic"

mqtt = Mqtt(app)
socketio = SocketIO(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(f"{mqtt_topic}/#")
    print("Connected to MQTT broker")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)
    socketio.emit(mqtt_to_socketio_topic, data=data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, use_reloader=False, debug=True)
