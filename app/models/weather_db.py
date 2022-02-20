from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.models import Base


class PastData(Base):
    __tablename__ = 'past_data'
    __table_args__ = {'schema': 'public'}

    past_id: int = Column(Integer(), primary_key=True)
    dt: int = Column(Integer())
    sunrise: int = Column(Integer())
    sunset: int = Column(Integer())
    temp: float = Column(Float())
    feels_like: float = Column(Float())
    pressure: float = Column(Float())
    humidity: float = Column(Float())
    dew_point: float = Column(Float())
    clouds: float = Column(Float())
    uvi: float = Column(Float())
    visibility: float = Column(Float())
    wind_speed: float = Column(Float())
    wind_gust: float = Column(Float())
    wind_deg: float = Column(Float())
    rain: float = Column(Float())
    snow: float = Column(Float())


class PastWeather(Base):
    __tablename__ = 'past_weather'
    __table_args__ = {'schema': 'public'}

    id: int = Column(Integer(), primary_key=True)
    past_id: int = Column(Integer(),
                          ForeignKey('public.past_data.past_id'),
                          nullable=False)
    weather_id: int = Column(Integer())
    main: str = Column(String())
    description: str = Column(String())
    icon: str = Column(String())


class HourData(Base):
    __tablename__ = 'hour_data'
    __table_args__ = {'schema': 'public'}

    hour_id: int = Column(Integer(), primary_key=True)
    dt: int = Column(Integer())
    hour_temp: float = Column(Float())
    feels_like: float = Column(Float())
    pressure: float = Column(Float())
    humidity: float = Column(Float())
    dew_point: float = Column(Float())
    uvi: float = Column(Float())
    clouds: float = Column(Float())
    visibility: float = Column(Float())
    wind_speed: float = Column(Float())
    wind_deg: float = Column(Float())
    wind_gust: float = Column(Float())
    pop: float = Column(Float())
    rain_1h: float = Column(Float())
    show_1h: float = Column(Float())


class DayData(Base):
    __tablename__ = 'day_data'
    __table_args__ = {'schema': 'public'}

    day_id: int = Column(Integer(), primary_key=True)
    dt: int = Column(Integer())
    sunrise: int = Column(Integer())
    sunset: int = Column(Integer())
    moonrise: int = Column(Integer())
    moonset: int = Column(Integer())
    moon_phase: float = Column(Float())
    pressure: float = Column(Float())
    humidity: float = Column(Float())
    dew_point: float = Column(Float())
    wind_gust: float = Column(Float())
    wind_speed: float = Column(Float())
    wind_deg: float = Column(Float())
    clouds: float = Column(Float())
    pop: float = Column(Float())
    rain: float = Column(Float())
    snow: float = Column(Float())
    uvi: float = Column(Float())


class HourWeather(Base):
    __tablename__ = 'hour_weather'
    __table_args__ = {'schema': 'public'}

    id: int = Column(Integer(), primary_key=True)
    hour_id: int = Column(Integer(),
                          ForeignKey('public.hour_data.hour_id'),
                          nullable=False)
    weather_id: int = Column(Integer())
    main: str = Column(String())
    description: str = Column(String())
    icon: str = Column(String())


class DayWeather(Base):
    __tablename__ = 'day_weather'
    __table_args__ = {'schema': 'public'}

    id: int = Column(Integer(), primary_key=True)
    day_id: int = Column(Integer(),
                         ForeignKey('public.day_data.day_id'),
                         nullable=False)
    weather_id: int = Column(Integer())
    main: str = Column(String())
    description: str = Column(String())
    icon: str = Column(String())


class DayTemperature(Base):
    __tablename__ = 'day_temperature'
    __table_args__ = {'schema': 'public'}

    id: int = Column(Integer(), primary_key=True)
    day_id: int = Column(Integer(),
                         ForeignKey('public.day_data.day_id'),
                         nullable=False)
    morn: float = Column(Float())
    day: float = Column(Float())
    day_min: float = Column(Float())
    day_max: float = Column(Float())
    eve: float = Column(Float())
    night: float = Column(Float())


class DayFeelsLike(Base):
    __tablename__ = 'day_feels_like'
    __table_args__ = {'schema': 'public'}

    id: int = Column(Integer(), primary_key=True)
    day_id: int = Column(Integer(),
                         ForeignKey('public.day_data.day_id'),
                         nullable=False)
    morn: float = Column(Float())
    day: float = Column(Float())
    eve: float = Column(Float())
    night: float = Column(Float())
