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


def future_weather_data(lat: str, lon: str,
                        dt: int, time_range: str):
    """
    Future weather forecast
    - if time_range == hourly: +48 hours
    - if time_range == daily: +7 days

    :param lat:
    :param lon:
    :param dt:
    :param time_range: 'hourly' or 'daily'
    :return: json - weather data
    """

    one_api = (os.getenv('ONE_CALL_API') + 'lat=' + str(lat)
               + '&lon=' + str(lon) + '&appid=' + API_KEY)
    one_api_result = requests.get(one_api).json()

    weather_list = one_api_result[time_range]

    # dts
    weather_dts = [weather['dt'] for weather in weather_list]

    nearest_value = get_nearest_value(weather_dts, dt)
    nearest_value_index = weather_dts.index(nearest_value)
    weather = weather_list[nearest_value_index]
    return weather


def get_nearest_value(iter_obj, value):
    """
    Finding the closest value to a given value in a list

    :param iter_obj:
    :param value:
    :return: closest value to value of type int
    """

    return min(iter_obj, key=lambda x: abs(x - value))


def check_missed_values(result_weather):
    """
    checking for values that might be missing

    :param result_weather: json weather data
    :return: wind_gust, snow, rain
    """

    # check wind_gust
    if 'wind_gust' in result_weather:
        wind_gust = result_weather['wind_gust']
    else:
        wind_gust = 0.0

    # check snow
    if 'snow' in result_weather:
        snow = result_weather['snow']
    else:
        snow = 0.0

    # check rain
    if 'rain' in result_weather:
        rain = result_weather['rain']
    else:
        rain = 0.0

    return wind_gust, snow, rain
