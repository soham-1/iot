import eventlet
from flask import Flask, render_template, request, session, redirect
from time import sleep
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import ssl
import json
import math

eventlet.monkey_patch()

CA = 'AmazonRootCA1.pem'
CERTI = '59a343ef7b-certificate.pem.crt'
KEYFILE = '59a343ef7b-private.pem.key'
# mqtt = mqtt.Client()
# mqtt.tls_set(CA, CERTI, KEYFILE, cert_reqs = ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers = None)
# mqtt.connect("a40rhj9y53gub-ats.iot.us-east-2.amazonaws.com", 8883, 60)

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'a40rhj9y53gub-ats.iot.us-east-2.amazonaws.com'
app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_REFRESH_TIME'] = 1.0
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_TLS_INSECURE'] = True
app.config['MQTT_TLS_CA_CERTS'] = CA
app.config['MQTT_TLS_CERTFILE'] = CERTI
app.config['MQTT_TLS_KEYFILE'] = KEYFILE


mqtt = Mqtt(app)
socketio = SocketIO(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("resource code" + str(rc))
    mqtt.subscribe("mytopic2", 0)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print((msg.payload).decode("utf-8"))
    print(message.payload)
    print(message.topic)
    print(1)
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # emit a mqtt_message event to the socket containing the message data
    socketio.emit('mqtt_message', data=data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

@app.route('/')
def index():
    return render_template('index.html')

socketio.run(app, host='localhost', port=5000, use_reloader=True, debug=True)