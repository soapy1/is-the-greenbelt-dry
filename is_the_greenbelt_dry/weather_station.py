import urllib3
import json
from datetime import date, timedelta, datetime
from functools import lru_cache
import pytz

from is_the_greenbelt_dry.constants import (
    API_BASE_URL,
    HISTORY_ENDPOINT,
    CURRENT_ENDPONT,
    SEVEN_DAY_SUMMARY_ENDPOINT,
)


class WeatherStation:
    def __init__(
        self,
        api_key,
        station_id,
        response_format="json",
        units="e",
        date_format="%Y%m%d",
    ):
        self.api_key = api_key
        self.station_id = station_id
        self.response_format = response_format
        self.units = units
        self.date_format = date_format
        self.units_key = "imperial" if units == "e" else "metric"

    def get_current_conditions(self):
        current_url = "{url_base}{endpoint}".format(
            url_base=API_BASE_URL, endpoint=CURRENT_ENDPONT
        )
        query_parameters = {
            "stationId": self.station_id,
            "format": self.response_format,
            "units": self.units,
            "apiKey": self.api_key,
        }
        http = urllib3.PoolManager()
        current_req = http.request("GET", current_url, fields=query_parameters)
        current_data = json.loads(current_req.data)
        return current_data.get("observations")

    @lru_cache
    def get_history_condition(self, date):
        history_url = "{url_base}{endpoint}".format(
            url_base=API_BASE_URL, endpoint=HISTORY_ENDPOINT
        )
        query_parameters = {
            "stationId": self.station_id,
            "format": self.response_format,
            "units": self.units,
            "apiKey": self.api_key,
            "date": date,
        }
        http = urllib3.PoolManager()
        history_req = http.request("GET", history_url, fields=query_parameters)
        history_data = json.loads(history_req.data)
        return history_data.get("observations")

    def extract_data_points(self, current_date_data, last_date_data):
        data_points = []
        previous_day_percip_total = sum(
            [d.get(self.units_key).get("precipTotal") for d in last_date_data]
        )
        combined_data = last_date_data + current_date_data
        for index, point in enumerate(combined_data[len(combined_data) - 24 :]):
            data_point = {}
            last_four_hours = combined_data[index - 3 : index + 1]
            data_point["date"] = point.get("obsTimeLocal")
            data_point["last_4_dewpt_avg"] = (
                sum([d.get(self.units_key).get("dewptAvg") for d in last_four_hours])
                / 4.0
            )
            data_point["last_4_temp_avg"] = (
                sum([d.get(self.units_key).get("tempAvg") for d in last_four_hours])
                / 4.0
            )
            data_point["last_4_solar_radiation_high"] = (
                sum([d.get("solarRadiationHigh") for d in last_four_hours]) / 4.0
            )
            data_point["last_4_humidity_avg"] = (
                sum([d.get("humidityAvg") for d in last_four_hours]) / 4.0
            )
            data_point["current_solar_radiation"] = point.get("solarRadiationHigh")
            data_point["current_humidity"] = point.get("humidityAvg")
            data_point["current_temp"] = point.get(self.units_key).get("tempAvg")
            data_point["current_dewpt"] = point.get(self.units_key).get("dewptAvg")
            data_point["current_precip_rate"] = point.get(self.units_key).get(
                "precipRate"
            )
            data_point["previous_day_percip_total"] = previous_day_percip_total
            data_points.append(data_point)
        return data_points

    @lru_cache
    def get_weather_features(self, target_date):
        last_date = target_date - timedelta(days=1)

        target_date_data = self.get_history_condition(
            target_date.strftime(self.date_format)
        )
        last_date_data = self.get_history_condition(
            last_date.strftime(self.date_format)
        )
        return self.extract_data_points(target_date_data, last_date_data)

    @lru_cache
    def last_three_days(self):
        summary_url = "{url_base}{endpoint}".format(
            url_base=API_BASE_URL, endpoint=SEVEN_DAY_SUMMARY_ENDPOINT
        )
        query_parameters = {
            "stationId": self.station_id,
            "format": self.response_format,
            "units": self.units,
            "apiKey": self.api_key,
        }
        http = urllib3.PoolManager()
        summary_req = http.request("GET", summary_url, fields=query_parameters)
        summary_data = json.loads(summary_req.data)
        daily_data = summary_data.get("summaries")

        # extract desired data from last three days
        last_three_days = [
            {
                "obsTimeLocal": i["obsTimeLocal"].split(" ")[0],
                "solarRadiation": i["solarRadiationHigh"],
                "tempHigh": i[self.units_key]["tempHigh"],
                "precipTotal": i[self.units_key]["precipTotal"],
            }
            for i in daily_data[-3:]
        ]

        return last_three_days
