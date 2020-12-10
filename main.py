from flask import Flask, render_template, request, session, redirect
import paho.mqtt.client as mqtt
import ssl
import json
import math
import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO



app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
ca_cert = 'AmazonRootCA1.pem'
certfile = '59a343ef7b-certificate.pem.crt'
keyfile = '59a343ef7b-private.pem.key'
mqtt_url = 'a40rhj9y53gub-ats.iot.us-east-2.amazonaws.com'


@app.route('/')
def homepage():
    context = {'data': [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]}
    speed = 20
    return render_template('charts_echart_basic.html', context=context,speed=x)


eventlet.monkey_patch()

app = Flask(__name__, template_folder='./views')
app.config['MQTT_BROKER_URL'] = mqtt_url
app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_REFRESH_TIME'] = 1.0
app.config['MQTT_TLS_CA_CERTS'] = ca_cert
app.config['MQTT_TLS_CERTFILE'] = certfile
app.config['MQTT_TLS_KEYFILE'] = keyfile

mqtt = Mqtt(app)
socketio = SocketIO(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('mytopic2')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = (message.payload).decode("utf-8")
    # emit a mqtt_message event to the socket containing the message data
    print(data)
    socketio.emit('mqtt_message', data=data)

@app.route('/')
def index():
    return render_template('index.html')

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

socketio.run(app, host='localhost', port=5000, use_reloader=True, debug=True)





# @app.route('/')
# def homepage1():

#     def on_connect(c, u, f, rc):
#         mqtt.subscribe("mytopic2", 0)

#     def on_message(c , u, msg):
#     # b'1' data fom bytes to string using utf-8
#         print((msg.payload).decode("utf-8"))
#         item = (msg.payload).decode("utf-8")
#         res = json.loads(item)
#         Activity = res["Activity"]
#         accler_x = res["accleration_x"]
#         accler_y = res["accleration_y"]
#         accler_z = res["accleration_y"]
#         calories=100
#         times_run =10
#         time_walk =20
#         if Activity==1:
#             def get_met(val):
#                 if val<=4:
#                     return 6
#                 elif val<=10:
#                     return 10
#                 else:
#                     return 15
#             times=0
#             speed = math.sqrt(pow(accler_x,2)+pow(accler_y,2)+pow(accler_z,2))
#             print("speed in m/s:%d , spped in km/hr:%d",speed,speed*3.6)
#             met = get_met(speed)
#             calories += 70 * met * (times_run/360)
#             print("Calories burned in run %d",calories)
#         else:
#             def get_met(val):
#                 if val<=4:
#                     return 6
#                 elif val<=10:
#                     return 10
#                 else:
#                     return 15
#             times=0
#             speed = math.sqrt(pow(accler_x,2)+pow(accler_y,2)+pow(accler_z,2))
#             print("speed in m/s:%d , spped in km/hr:%d",speed,speed*3.6)
#             met = get_met(speed)
#             calories += 70 * met * (time_walk/360)
#             print("Calories burned in walk %d",calories)
#     CA = 'AmazonRootCA1.pem'
#     CERTI = '59a343ef7b-certificate.pem.crt'
#     KEYFILE = '59a343ef7b-private.pem.key'
#     mqtt = mqtt.Client()
#     mqtt.tls_set(CA, CERTI, KEYFILE, cert_reqs = ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers = None)
#     mqtt.connect("a40rhj9y53gub-ats.iot.us-east-2.amazonaws.com", 8883, 60)
#     mqtt.on_connect = on_connect
#     mqtt.on_message = on_message
#     mqtt.loop_forever()
#     return speed

app.run(debug=True)