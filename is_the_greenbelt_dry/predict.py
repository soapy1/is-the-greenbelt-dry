import os
from datetime import date
from is_the_greenbelt_dry.weather_station import WeatherStation
from is_the_greenbelt_dry.constants import SOUTH_AUSTIN_STATION_ID


API_KEY = os.environ.get("WEATHER_API_KEY")


def predict_if_greenbelt_dry():
    ws = WeatherStation(API_KEY, SOUTH_AUSTIN_STATION_ID)
    current_conditions = ws.get_current_conditions()
    target_date = date.today()
    current_weather_features = ws.get_weather_features(target_date)

    latest_data_point = current_weather_features[-1]
    # It's currently raining
    if latest_data_point.get("current_precip_rate") > 0:
        msg = "currently raining, greenbelt is moist af"
        greenbelt_dry = False
    # It's currently not raining
    else:
        # It didn't rain yesterday
        if latest_data_point.get("previous_day_percip_total") == 0:
            msg = "hasn't rained in  while, greenbelt is probably dry"
            greenbelt_dry = True
        # It did rain yesterday
        else:
            # High temp + high solar radiation means the rock will dry well
            if (
                latest_data_point.get("last_4_dewpt_avg")
                < latest_data_point.get("last_4_temp_avg")
            ) and (latest_data_point.get("last_4_solar_radiation_high") > 400):
                msg =  "it recently rained, but there is a chance that the greenbelt is dry enough"
                greenbelt_dry = True
            else:
                msg = "it recently rained and hasn't been very sunny, the greenbelt is probably wet"
                greenbelt_dry = False
    return msg, greenbelt_dry
