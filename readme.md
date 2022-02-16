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
git clone https://github.com/IvanSerebryakov/WeatherAPI.git
```
3. Activate venv
```
source venv/bin/activate
```
4. Install all dependencies from requirements.txt to venv
```
pip install -r requirements.txt
```
5. Create `.env` file in your root dir and set env variables:
```commandline
export API_KEY={your api key from OpenWeather API}
export GEOCODING_API={geocoding api from OpenWeather API}
export ONE_CALL_API={one call api from OpenWeather API}
export HISTORY_API={one call api for hystory data from OpenWeather API}
export WEATHER_API_URI={uri for database connecting postgresql://{user}:{passsword}@{host}:{port}/{db}}
```
6. Run command:
```commandline
source .env
```
7. Run project from /my_app dir by uvicorn
```
uvicorn app:app --reload
```

