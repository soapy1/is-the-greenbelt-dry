import os
from datetime import date
from weather_station import WeatherStation


API_KEY = os.environ.get("WEATHER_API_KEY")
# Station for Bouldin - South Austin
# https://www.wunderground.com/dashboard/pws/KTXAUSTI90
STATION_ID = "KTXAUSTI90"


def main():
    ws = WeatherStation(API_KEY, STATION_ID)
    current_conditions = ws.get_current_conditions()
    target_date = date(2020, 3, 9)
    current_weather_features = ws.get_weather_features(target_date)

    latest_data_point = current_weather_features[-1]
    # It's currently raining
    if latest_data_point.get("current_precip_rate") > 0:
        print("currently raining, no greenbelt")
    # It's currently not raining
    else:
        # It didn't rain yesterday
        if latest_data_point.get("previous_day_percip_total") == 0:
            print("hasn't rained in  while, greenbelt is probably dry")
        # It did rain yesterday
        else:
            # High temp + high solar radiation means the rock will dry well
            if (
                latest_data_point.get("last_4_dewpt_avg")
                < latest_data_point.get("last_4_temp_avg")
            ) and (latest_data_point.get("last_4_solar_radiation_high") > 400):
                print(
                    "it recently rained, but there is a change that the greenbelt is dry enough"
                )
            else:
                print(
                    "it recently rained and hasn't been very sunny, the greenbelt is probably wet"
                )


if __name__ == "__main__":
    main()
