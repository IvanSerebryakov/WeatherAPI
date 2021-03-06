from app.models.weather_db import HourData

from app import app
from app.models import (pg_scoped_factory,
                        DayData,
                        PastData,
                        PastWeather,
                        HourWeather,
                        DayWeather,
                        DayTemperature,
                        DayFeelsLike)
from app.utils.api_utils import (get_lat_lon,
                                 get_now_by_lat_lon,
                                 past_weather_data,
                                 future_weather_data,
                                 check_missed_values)
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
        sunrise = result_weather['sunrise']
        sunset = result_weather['sunset']
        temp = result_weather['temp']
        feels_like = result_weather['feels_like']
        pressure = result_weather['pressure']
        humidity = result_weather['humidity']
        dew_point = result_weather['dew_point']
        clouds = result_weather['clouds']
        uvi = result_weather['uvi']
        visibility = result_weather['visibility']
        wind_speed = result_weather['wind_speed']
        wind_gust, snow, rain = check_missed_values(result_weather)
        wind_deg = result_weather['wind_deg']

        # commit in past data
        past_data = PastData(dt=dt,
                             sunrise=sunrise,
                             sunset=sunset,
                             temp=temp,
                             feels_like=feels_like,
                             pressure=pressure,
                             humidity=humidity,
                             dew_point=dew_point,
                             clouds=clouds,
                             uvi=uvi,
                             visibility=visibility,
                             wind_speed=wind_speed,
                             wind_gust=wind_gust,
                             wind_deg=wind_deg,
                             rain=rain,
                             snow=snow)
        weather_api_db.add(past_data)
        weather_api_db.commit()

        # commit in past weather
        past_result_weather = result_weather['weather'][0]
        weather_id = past_result_weather['id']
        main = past_result_weather['main']
        description = past_result_weather['description']
        icon = past_result_weather['icon']

        past_weather = PastWeather(past_id=past_data.past_id,
                                   weather_id=weather_id,
                                   main=main,
                                   description=description,
                                   icon=icon)
        weather_api_db.add(past_weather)
        weather_api_db.commit()
        weather_api_db.close()

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

        # check wind_gust
        if 'wind_gust' in result_weather:
            wind_gust = result_weather['wind_gust']
        else:
            wind_gust = 0.0

        pop = result_weather['pop']

        # check rain
        if 'rain' in result_weather:
            rain_1h = result_weather['rain']['1h']
        else:
            rain_1h = 0.0

        # check snow
        if 'snow' in result_weather:
            snow_1h = result_weather['rain']['1h']
        else:
            snow_1h = 0.0

        # commit in hour data
        hour_data = HourData(dt=dt,
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
                             wind_gust=wind_gust,
                             pop=pop,
                             rain_1h=rain_1h,
                             snow_1h=snow_1h)

        weather_api_db.add(hour_data)
        weather_api_db.commit()

        # commit in hour weather
        weather_id = result_weather['weather']['id']
        main = result_weather['weather']['main']
        description = result_weather['weather']['description']
        icon = result_weather['weather']['icon']

        hour_weather = HourWeather(hour_id=hour_data.hour_id,
                                   weather_id=weather_id,
                                   main=main,
                                   description=description,
                                   icon=icon)
        weather_api_db.add(hour_weather)
        weather_api_db.commit()
        weather_api_db.close()

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
        wind_gust, snow, rain = check_missed_values(result_weather)
        uvi = result_weather['uvi']

        # commit in day data
        day_data = DayData(dt=dt,
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
                           uvi=uvi,
                           wind_gust=wind_gust)

        weather_api_db.add(day_data)
        weather_api_db.commit()

        # commit in day weather
        weather_id = result_weather['weather']['id']
        main = result_weather['weather']['main']
        description = result_weather['weather']['description']
        icon = result_weather['weather']['icon']

        day_weather = DayWeather(day_id=day_data.day_id,
                                 weather_id=weather_id,
                                 main=main,
                                 description=description,
                                 icon=icon)
        weather_api_db.add(day_weather)
        weather_api_db.commit()

        # commit in day temp
        morn = result_weather['temp']['morn']
        day = result_weather['temp']['day']
        day_min = result_weather['temp']['min']
        day_max = result_weather['temp']['max']
        eve = result_weather['temp']['eve']
        night = result_weather['temp']['night']

        day_temperature = DayTemperature(day_id=day_data.day_id,
                                         morn=morn,
                                         day=day,
                                         day_min=day_min,
                                         day_max=day_max,
                                         eve=eve,
                                         night=night)
        weather_api_db.add(day_temperature)
        weather_api_db.commit()

        # commit in day feels like
        morn = result_weather['feels_like']['morn']
        day = result_weather['feels_like']['day']
        eve = result_weather['feels_like']['eve']
        night = result_weather['feels_like']['night']

        day_feels_like = DayFeelsLike(day_id=day_data.day_id,
                                      morn=morn,
                                      day=day,
                                      eve=eve,
                                      night=night)

        weather_api_db.add(day_feels_like)
        weather_api_db.commit()
        weather_api_db.close()

    return {'result_weather': result_weather}
