from flask import Flask, render_template
from is_the_greenbelt_dry.predict import predict_if_greenbelt_dry

app = Flask(__name__)

@app.route('/')
def is_the_greenbelt_dry():
    msg, greenbelt_dry = predict_if_greenbelt_dry()
    return render_template('dry.html', msg=msg, greenbelt_dry=greenbelt_dry)
