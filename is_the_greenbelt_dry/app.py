import os
from flask import Flask, render_template
from is_the_greenbelt_dry.predict import predict_if_greenbelt_dry
from is_the_greenbelt_dry.weather_station import WeatherStation
from is_the_greenbelt_dry.constants import SOUTH_AUSTIN_STATION_ID

app = Flask(__name__)

API_KEY = os.environ.get("WEATHER_API_KEY")

@app.route('/')
def is_the_greenbelt_dry():
    msg, greenbelt_dry = predict_if_greenbelt_dry()
    ws = WeatherStation(API_KEY, SOUTH_AUSTIN_STATION_ID)
    weather_summary = ws.last_three_days()
    return render_template(
        'dry.html', 
        msg=msg, 
        greenbelt_dry=greenbelt_dry, 
        weather_summary=weather_summary
    )
