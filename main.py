from flask import Flask, render_template, request, session, redirect, g
import random
import time
from time import sleep

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

@app.route('/')
def homepage():
    context = {'data': [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]}
    speed = random.random()
    g.s = simple()
    return render_template('charts_echart_basic.html', context=context, speed=speed)

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
