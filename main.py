from flask import Flask, render_template, request, session, redirect
from time import sleep

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

# @app.route('/')
# def homepage():
#     context = {'data': [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]}
#     speed = 20
#     return render_template('charts_echart_basic.html', context=context,speed=speed)



@app.route('/')
def homepage():
    import paho.mqtt.client as mqtt
    import ssl
    import json
    import math
    CA = 'AmazonRootCA1.pem'
    CERTI = '59a343ef7b-certificate.pem.crt'
    KEYFILE = '59a343ef7b-private.pem.key'
    mqtt = mqtt.Client()
    mqtt.tls_set(CA, CERTI, KEYFILE, cert_reqs = ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers = None)
    mqtt.connect("a40rhj9y53gub-ats.iot.us-east-2.amazonaws.com", 8883, 60)

    
    def on_connect(c, u, f, rc):
        print("resource code" + str(rc))
        mqtt.subscribe("mytopic2", 0)

    def on_message(c , u, msg):
    # b'1' data fom bytes to string using utf-8
        print((msg.payload).decode("utf-8"))
        item = (msg.payload).decode("utf-8")
        res = json.loads(item)
        Activity = res["Activity"]
        accler_x = res["accleration_x"]
        accler_y = res["accleration_y"]
        accler_z = res["accleration_y"]
        calories=100
        times_run =10
        time_walk =20
        if Activity==1:
            def get_met(val):
                if val<=4:
                    return 6
                elif val<=10:
                    return 10
                else:
                    return 15
            times=0
            speed = math.sqrt(pow(accler_x,2)+pow(accler_y,2)+pow(accler_z,2))
            print("speed in m/s:%d , spped in km/hr:%d",speed,speed*3.6)
            met = get_met(speed)
            calories += 70 * met * (times_run/360)
            print("Calories burned in run %d",calories)
        else:
            def get_met(val):
                if val<=4:
                    return 6
                elif val<=10:
                    return 10
                else:
                    return 15
            times=0
            speed = math.sqrt(pow(accler_x,2)+pow(accler_y,2)+pow(accler_z,2))
            print("speed in m/s:%d , spped in km/hr:%d",speed,speed*3.6)
            met = get_met(speed)
            calories += 70 * met * (time_walk/360)
            print("Calories burned in walk %d",calories)
        mqtt.on_connect = on_connect
        mqtt.on_message = on_message
        mqtt.loop_forever()
    return render_template('charts_echart_basic.html')

def simple():
    sec = time.time()
    print(sec)
    end = time.time()
    print(end-sec)
    print("hello")
    return end

@app.route('/counter')
def counter():
    return render_template('component_counter.html')

@app.route('/stream')
def stream():
    def generate():
        print("recicev")
        mylist = range(3)
        for i in mylist:
            yield str(i*i)
        # while True:
        #     yield "a"
            sleep(1)

    return app.response_class(generate(), mimetype='text/plain')
# app.run(debug=True)
if __name__ == '__main__':
    # socketio.run(app)
    app.run(debug=True)
