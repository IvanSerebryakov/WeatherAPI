import datetime
import os

import pytz
import requests
from timezonefinder import TimezoneFinder

API_KEY = os.getenv('API_KEY')


def get_now_by_lat_lon(lat: int, lon: int):
    """
    Getting timezone and current time
    according to the corresponding timezone

    :param lat: latitude
    :param lon: longitude
    :return:
    --timezone example 'Europe/Moscow', now format DateTime
    """

    tf = TimezoneFinder(in_memory=True)
    time_zone = tf.timezone_at(lng=lon, lat=lat)
    now = datetime.datetime.now(pytz.timezone(time_zone))
    return time_zone, now


def get_lat_lon(city: str, country_code: str):
    """
    Getting latitude and longitude

    :param city:
    :param country_code: format iso 3166
    :return: lat, lon
    """

    geocoding_api = (os.getenv('GEOCODING_API') +
                     'q=' + city + ',' + country_code
                     + '&appid=' + API_KEY)

    response = requests.get(geocoding_api).json()
    lat = response[0]['lat']
    lon = response[0]['lon']

    return lat, lon


def past_weather_data(lat: str, lon: str, dt: str):
    """
    Historical weather data

    :return: json - past weather data (max: -5 days)
    """

    history_api = (os.getenv('HISTORY_API') + 'lat=' + lat
                   + '&lon=' + lon + '&dt=' + dt
                   + '&appid=' + API_KEY)
    history_api_result = requests.get(history_api).json()
    current_block = history_api_result['current']

    return current_block


def now_weather_data(lat: str, lon: str):
    """
    Current weather forecast

    :return: json - weather data
    """

    one_api = (os.getenv('ONE_CALL_API') + 'lat=' + str(lat)
               + '&lon=' + str(lon) + '&appid=' + API_KEY)
    one_api_result = requests.get(one_api).json()
    current_weather_json = one_api_result['current']
    return current_weather_json


def future_hour_weather_data(lat: str, lon: str, dt: int):
    """
    Future weather forecast
    - hourly +48 hours

    :return: json - weather data
    """

    one_api = (os.getenv('ONE_CALL_API') + 'lat=' + str(lat)
               + '&lon=' + str(lon) + '&appid=' + API_KEY)
    one_api_result = requests.get(one_api).json()

    hourly_weather_list = one_api_result['hourly']

    # dts
    hourly_weather_dts = [hourly_weather['dt'] for hourly_weather
                          in hourly_weather_list]

    nearest_value = get_nearest_value(hourly_weather_dts, dt)
    nearest_value_index = hourly_weather_dts.index(nearest_value)
    hour_weather = hourly_weather_list[nearest_value_index]
    return hour_weather


def future_day_weather_data(lat: str, lon: str, dt: int):
    """
    Future weather forecast
    - daily +7 days

    :return: json - weather data
    """

    one_api = (os.getenv('ONE_CALL_API') + 'lat=' + str(lat)
               + '&lon=' + str(lon) + '&appid=' + API_KEY)
    one_api_result = requests.get(one_api).json()
    daily_weather_list = one_api_result['daily']

    daily_weather_dts = [daily_weather['dt'] for daily_weather
                         in daily_weather_list]
    nearest_value = get_nearest_value(daily_weather_dts, dt)
    nearest_value_index = daily_weather_dts.index(nearest_value)
    day_weather = daily_weather_list[nearest_value_index]
    return day_weather


def get_nearest_value(iter_obj, value):
    """
    Finding the closest value to a given value in a list

    :param iter_obj:
    :param value:
    :return: closest value to value of type int
    """

    return min(iter_obj, key=lambda x: abs(x - value))
