from app import app
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

    if days_diff < 0:
        result_weather = past_weather_data(lat=str(lat), lon=str(lon),
                                           dt=str(int(dt)))
    elif 0 < days_diff <= 2:
        result_weather = future_weather_data(lat=str(lat), lon=str(lon),
                                             dt=int(dt), time_range='hourly')
    else:
        result_weather = future_weather_data(lat=str(lat), lon=str(lon),
                                             dt=int(dt), time_range='daily')

    return {'result_weather': result_weather}
