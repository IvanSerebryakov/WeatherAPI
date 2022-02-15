import datetime

import dateutil.parser
import pytz


def get_datetime_by_utctime(dt: int):
    """
    Convert UTC epoch time to DateTime format

    :param dt: epoch time UTC
    :return: converted UTC epoch time to DateTime format
    """

    date_time = datetime.datetime.fromtimestamp(dt)
    return date_time


def get_utctime_by_datetime(year: int, month: int, day: int,
                            hour: int, tz_info: str):
    """
    Getting timestamp from UTC

    :param year:
    :param month:
    :param day:
    :param hour:
    :param tz_info: timezone example: 'Europe/Moscow'
    :return:
    """

    dt = datetime.datetime(year, month, day, hour)
    tz = pytz.timezone(tz_info)
    timestamp = dt.replace(tzinfo=tz).timestamp()
    return timestamp


def iso_date_parser(year: str, month: str, date: str):
    """
    Date generation in ISO format

    :param date: date type - dayTHH:mm
    :param year:
    :param month:
    :return: date type - yy-MM-dd
    """

    user_date = dateutil.parser.isoparse(year + '-'
                                         + month.zfill(2) + '-'
                                         + date)
    return user_date



