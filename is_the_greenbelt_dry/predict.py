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
    target_date = date(2020, 2, 11)
    current_weather_features = ws.get_weather_features(target_date)
    print(current_weather_features)

if __name__ == '__main__':
    main()
