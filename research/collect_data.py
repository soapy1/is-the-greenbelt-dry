#
# API endpoint ex: https://api.weather.com/v2/pws/history/hourly?stationId=KTXAUSTI90&format=json&units=m&apiKey=qwer1234asdf&date=20200311
#
# Initial varaibles:
#   current:
#       solarRadiation, humidity, temp, dewpt, precipRate
#   previous day:
#       precipTotal
#   last 4 hours:
#       solarRadiationHigh, humidityAvg, tempAvg, dewptAvg

import urllib3
import os
import json
from datetime import date, timedelta
import csv


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

DATE_FORMAT = "%Y%m%d"


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
    return current_data.get("observations")


def get_history_condition(date):
    history_url = "{url_base}{endpoint}".format(
        url_base=API_BASE_URL, endpoint=HISTORY_ENDPOINT
    )
    query_parameters = {
        "stationId": STATION_ID,
        "format": RESPONSE_FORMAT,
        "units": UNITS,
        "apiKey": API_KEY,
        "date": date,
    }

    http = urllib3.PoolManager()

    history_req = http.request("GET", history_url, fields=query_parameters)
    history_data = json.loads(history_req.data)
    return history_data.get("observations")


def extract_data_points(current_date_data, last_date_data):
    data_points = []
    previous_day_percip_total = sum(
        [d.get("metric").get("precipTotal") for d in last_date_data]
    )
    combined_data = last_date_data + current_date_data
    for index, point in enumerate(combined_data[len(last_date_data) :]):
        data_point = {}
        last_four_hours = combined_data[index - 3 : index + 1]
        data_point["date"] = point.get("obsTimeLocal")
        data_point["last_4_dewpt_avg"] = (
            sum([d.get("metric").get("dewptAvg") for d in last_four_hours]) / 4.0
        )
        data_point["last_4_temp_avg"] = (
            sum([d.get("metric").get("tempAvg") for d in last_four_hours]) / 4.0
        )
        data_point["last_4_solar_radiation_high"] = (
            sum([d.get("solarRadiationHigh") for d in last_four_hours]) / 4.0
        )
        data_point["last_4_humidity_avg"] = (
            sum([d.get("humidityAvg") for d in last_four_hours]) / 4.0
        )
        data_point["current_solar_radiation"] = point.get("solarRadiationHigh")
        data_point["current_humidity"] = point.get("humidityAvg")
        data_point["current_temp"] = point.get("metric").get("tempAvg")
        data_point["current_dewpt"] = point.get("metric").get("dewptAvg")
        data_point["current_precip_rate"] = point.get("metric").get("precipRate")
        data_point["previous_day_percip_total"] = previous_day_percip_total
        data_points.append(data_point)
    return data_points


def main():
    current_date = date(2020, 2, 11)
    last_date = current_date - timedelta(days=1)

    current_date_data = get_history_condition(current_date.strftime(DATE_FORMAT))
    last_date_data = get_history_condition(last_date.strftime(DATE_FORMAT))

    points = []
    for i in range(1, 21):
        points.extend(extract_data_points(current_date_data, last_date_data))
        last_date = current_date
        current_date = current_date + timedelta(days=1)
        last_date_data = current_date_data
        current_date_data = get_history_condition(current_date.strftime(DATE_FORMAT))

    with open("weather.csv", "w") as weather_file:
        fieldnames = [
            "date",
            "last_4_dewpt_avg",
            "last_4_temp_avg",
            "last_4_solar_radiation_high",
            "last_4_humidity_avg",
            "current_solar_radiation",
            "current_humidity",
            "current_temp",
            "current_dewpt",
            "current_precip_rate",
            "previous_day_percip_total",
        ]
        writer = csv.DictWriter(weather_file, fieldnames=fieldnames)
        writer.writeheader()
        for point in points:
            writer.writerow(point)


if __name__ == "__main__":
    main()
