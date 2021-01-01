import os
from datetime import date, datetime
import pytz
from is_the_greenbelt_dry.weather_station import WeatherStation
from is_the_greenbelt_dry.constants import SOUTH_AUSTIN_STATION_ID


API_KEY = os.environ.get("WEATHER_API_KEY")


def predict_if_greenbelt_dry():
    ws = WeatherStation(API_KEY, SOUTH_AUSTIN_STATION_ID)
    tz = pytz.timezone("America/Chicago")
    target_date = datetime.now(tz).date()
    current_weather_features = ws.get_weather_features(target_date)
    latest_data_point = current_weather_features[-1]

    current_day_rain = sum([i["current_precip_rate"] for i in current_weather_features])
    # It's currently raining
    if current_day_rain > 0.0:
        # It's currently raining
        if latest_data_point.get("current_precip_rate") > 0:
            msg = "currently raining, greenbelt is wet af"
            greenbelt_dry = False
        else:
            msg = "so far today it has rained %s inches, it's probably wet" % str(
                round(current_day_rain, 2)
            )
            greenbelt_dry = False
    # It's currently not raining
    else:
        # It didn't rain yesterday
        if latest_data_point.get("previous_day_percip_total") == 0:
            msg = "hasn't rained in  while, greenbelt is probably dry"
            greenbelt_dry = True
        # It did rain yesterday
        else:
            # It hasn't rained for the past 12 hours
            if set(
                w.get("current_precip_rate") for w in current_weather_features[12:]
            ) == {0.0}:
                msg = "it rained more than 12 hours ago, the greenbelt is probably dry enough"
                greenbelt_dry = True
            # High temp + high solar radiation means the rock will dry well
            elif (
                latest_data_point.get("last_4_dewpt_avg")
                < latest_data_point.get("last_4_temp_avg")
            ) and (latest_data_point.get("last_4_solar_radiation_high") > 400):
                msg = "it recently rained, but there is a chance that the greenbelt is dry enough"
                greenbelt_dry = True
            else:
                msg = "it recently rained and hasn't been very sunny, the greenbelt is probably moist"
                greenbelt_dry = False
    return msg, greenbelt_dry
