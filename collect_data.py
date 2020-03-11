#
# API endpoint ex: https://api.weather.com/v2/pws/history/hourly?stationId=KTXAUSTI90&format=json&units=m&apiKey=7bc0df6cb93347e680df6cb933b7e67d&date=20200311
#
# Initial varaibles:
#   current:
#       solarRadiationHigh, humidityAvg, tempAvg, dewptAvg,
#       precipRate
#   previous day:
#       precipTotal
#

import urllib3
import os
import json

API_BASE_URL = "https://api.weather.com"
HISTORY_ENDPOINT = "/v2/pws/history/hourly"
CURRENT_ENDPONT = "/v2/pws/observations/current"
API_KEY = os.environ.get("WEATHER_API_KEY")
# Station for Bouldin - South Austin
# https://www.wunderground.com/dashboard/pws/KTXAUSTI90
STATION_ID = "KTXAUSTI90"
RESPONSE_FORMAT = "json"
# Units in metric
UNITS = "m"


def get_current_conditions():
    current_url = "{url_base}{endpoint}".format(
        url_base=API_BASE_URL, endpoint=CURRENT_ENDPONT
    )
    query_parameters = {
        "stationId": STATION_ID,
        "format": RESPONSE_FORMAT,
        "units": UNITS,
        "apiKey": API_KEY,
    }

    http = urllib3.PoolManager()
    current_req = http.request("GET", current_url, fields=query_parameters)
    current_data = json.loads(current_req.data)


def main():
    history_url = "{url_base}{endpoint}".format(
        url_base=API_BASE_URL, endpoint=HISTORY_ENDPOINT
    )
    query_parameters = {
        "stationId": STATION_ID,
        "format": RESPONSE_FORMAT,
        "units": UNITS,
        "apiKey": API_KEY,
        "date": ""
    }

    http = urllib3.PoolManager()

    history_req = http.request("GET", history_url, fields=query_parameters)
    history_data = json.loads(history_req.data)


if __name__ == "__main__":
    main()
