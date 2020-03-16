from flask import Flask
from is_the_greenbelt_dry.predict import predict_if_greenbelt_dry

app = Flask(__name__)

@app.route('/')
def is_the_greenbelt_dry():
    predict_if_greenbelt_dry()
    return 'Hello, World!'
