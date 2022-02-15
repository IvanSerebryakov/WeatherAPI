import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

WEATHER_API_URI = os.getenv('WEATHER_API_URI')
pg_engine = create_engine(WEATHER_API_URI)

pg_session_factory = sessionmaker(bind=pg_engine)
pg_scoped_factory = scoped_session(pg_session_factory)

Base = declarative_base()

from app.models.weather_db import *

