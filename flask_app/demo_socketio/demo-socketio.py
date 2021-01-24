import eventlet
from eventlet import wsgi
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MQTT_BROKER_URL'] = 'mqtt.hpc.bg'
app.config['MQTT_BROKER_PORT'] = 1883
MQTT_TOPIC = 'controllers/#'

mqtt = Mqtt(app)
socketio = SocketIO(app)


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    socketio.emit(event='new_event', data=f'My data {str(json)}')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(MQTT_TOPIC)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):

    # payload = float(message.payload)
    topic = message.topic
    # print(topic)
    socketio.emit(event='new_event', data=topic)


@app.route('/')
def index():
    return render_template('client.html')


@app.route('/login_form', methods=['POST'])
def login_form():
    controller_id = request.form['controller_id']
    return render_template('login_form.html', controller_id=controller_id)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    name = request.form['name']
    controller_id = request.form['controller_id']
    return f'email: {email}, name: {name}, controller_id: {controller_id}'


if __name__ == '__main__':
    wsgi.server(eventlet.listen(('', 5000)), app, debug=True)
