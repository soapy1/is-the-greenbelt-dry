#
# API endpoint ex: https://api.weather.com/v2/pws/history/hourly?stationId=KTXAUSTI90&format=json&units=m&apiKey=7bc0df6cb93347e680df6cb933b7e67d&date=20200311
#

import urllib3
import os
import json

API_BASE_URL = "https://api.weather.com"
HISTORY_ENDPOINT = "/v2/pws/history/hourly"
API_KEY = os.environ.get("WEATHER_API_KEY")
# Station for Bouldin - South Austin
# https://www.wunderground.com/dashboard/pws/KTXAUSTI90
STATION_ID = "KTXAUSTI90"
RESPONSE_FORMAT = "json"
# Units in metric
UNITS = "m"


def main():
    url = "{url_base}{endpoint}".format(
        url_base=API_BASE_URL, endpoint=HISTORY_ENDPOINT
    )
    query_parameters = {
        "stationId": STATION_ID,
        "format": RESPONSE_FORMAT,
        "units": UNITS,
        "apiKey": API_KEY,
        "date": "20200311"
    }
    http = urllib3.PoolManager()
    req = http.request("GET", url, fields=query_parameters)
    data = json.loads(req.data)


if __name__ == "__main__":
    main()
