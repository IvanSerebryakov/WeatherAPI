# API for getting weather forecast data

Service that implements receiving weather data via API.
The API accepts a country code, a city, and a date with time as input.
The service should respond with weather information using the OpenWeather API.

## Example:

/weather?country_code=RU&city=Moscow&date=< день в диапазоне доступных дат >T12:00

Provides information about the weather for Moscow at 12:00 on the selected day

Save the received information and return it when requested again, without referring to the api of the weather service.


## Built with

This section lists the main technologies of the project

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Pytest

## Getting Started
Instructions for installing and running the project on your computer

1. Register on [https://openweathermap.org/](https://openweathermap.org/)
2. Clone the repo

```

```
3. Activate venv
```
source venv/bin/activate
```
4. Install all dependencies from requirements.txt to venv
```
pip install -r requirements.txt
```
5. Run project from /my_app dir by uvicorn
```
uvicorn app:app --reload
```

