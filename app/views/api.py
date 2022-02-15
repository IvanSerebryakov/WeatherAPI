import itertools

from app.models.weather_db import HourData

from app import app
from app.models import pg_scoped_factory, DayData
from app.utils.api_utils import (get_lat_lon,
                                 get_now_by_lat_lon,
                                 past_weather_data,
                                 future_weather_data)
from app.utils.datetime_utils import (get_utctime_by_datetime,
                                      iso_date_parser)


@app.get("/weather")
def weather(country_code: str, city: str, date: str):
    """
    API for getting weather forecast data

    --days_diff - the difference in the number of days of time,
      user entered and current time from UTC
     - if days_diff < 0: get history data
     - if 0 <= days_diff <= 2: get hourly data (+48 hours)
     - else get daily data (+7 days)

    :param country_code: example 'RU' (format iso 3166)
    :param city: example 'Moscow'
    :param date: format ddTHH:mm
    :return: json - weather data
    """

    # now
    lat, lon = get_lat_lon(city=city, country_code=country_code)
    time_zone, date_time_now = get_now_by_lat_lon(lat, lon)
    year_now = date_time_now.year
    month_now = date_time_now.month
    day_now = date_time_now.day

    # user data
    user_date = iso_date_parser(year=str(year_now), month=str(month_now),
                                date=date)

    # convert data to utc epoch
    dt = get_utctime_by_datetime(year=user_date.year, month=user_date.month,
                                 day=user_date.day, hour=user_date.hour,
                                 tz_info=time_zone)
    days_diff = user_date.day - day_now

    # db
    weather_api_db = pg_scoped_factory()

    if days_diff < 0:
        result_weather = past_weather_data(lat=str(lat), lon=str(lon),
                                           dt=str(int(dt)))
    elif 0 <= days_diff <= 2:
        result_weather = future_weather_data(lat=str(lat), lon=str(lon),
                                             dt=int(dt), time_range='hourly')
        temp = result_weather['temp']
        feels_like = result_weather['feels_like']
        pressure = result_weather['pressure']
        humidity = result_weather['humidity']
        dew_point = result_weather['dew_point']
        uvi = result_weather['uvi']
        clouds = result_weather['clouds']
        visibility = result_weather['visibility']
        wind_speed = result_weather['wind_speed']
        wind_deg = result_weather['wind_deg']
        wind_gust = result_weather['wind_gust']

        _id = next(itertools.count(1, 1))
        hour_id = next(itertools.count(60, 1))
        hour_data = HourData(id=_id,
                             hour_id=hour_id,
                             dt=dt,
                             hour_temp=temp,
                             feels_like=feels_like,
                             pressure=pressure,
                             humidity=humidity,
                             dew_point=dew_point,
                             uvi=uvi,
                             clouds=clouds,
                             visibility=visibility,
                             wind_speed=wind_speed,
                             wind_deg=wind_deg,
                             wind_gust=wind_gust)
        weather_api_db.add(hour_data)
        weather_api_db.commit()

    else:
        result_weather = future_weather_data(lat=str(lat), lon=str(lon),
                                             dt=int(dt), time_range='daily')

        sunrise = result_weather['sunrise']
        sunset = result_weather['sunset']
        moonrise = result_weather['moonrise']
        moonset = result_weather['moonset']
        moon_phase = result_weather['moon_phase']
        pressure = result_weather['pressure']
        humidity = result_weather['humidity']
        dew_point = result_weather['dew_point']
        wind_speed = result_weather['wind_speed']
        wind_deg = result_weather['wind_deg']
        clouds = result_weather['clouds']
        pop = result_weather['pop']
        if ('snow' in result_weather
                and 'rain' not in result_weather):
            snow = result_weather['snow']
            rain = 0.0
        elif ('rain' in result_weather
                and 'snow' not in result_weather):
            rain = result_weather['rain']
            snow = 0.0
        elif ('rain' in result_weather
                and 'snow' in result_weather):
            rain = result_weather['rain']
            snow = result_weather['snow']
        else:
            rain = 0.0
            snow = 0.0

        uvi = result_weather['uvi']

        _id = next(itertools.count(1, 1))
        day_id = next(itertools.count(60 * 24, 1))
        day_data = DayData(id=_id,
                           day_id=day_id,
                           dt=dt,
                           sunrise=sunrise,
                           sunset=sunset,
                           moonrise=moonrise,
                           moonset=moonset,
                           moon_phase=moon_phase,
                           pressure=pressure,
                           humidity=humidity,
                           dew_point=dew_point,
                           wind_speed=wind_speed,
                           wind_deg=wind_deg,
                           clouds=clouds,
                           pop=pop,
                           rain=rain,
                           snow=snow,
                           uvi=uvi)
        weather_api_db.add(day_data)
        weather_api_db.commit()

    return {'result_weather': result_weather}
