from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)

@app.route('/')
def homepage():
    context = {'data': [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]}
    return render_template('charts_echart_basic.html', context=context)

app.run(debug=True)