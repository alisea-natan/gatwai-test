import os

import requests
from dotenv import load_dotenv
import datetime


def weather_in_kyiv():
    load_dotenv()

    API_KEY = os.getenv("WEATHER_API")
    CITY_ID = 703448

    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&appid={API_KEY}"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?id={CITY_ID}&appid={API_KEY}"

    response = requests.get(current_weather_url)
    if response.status_code == 200:
        current_weather_data = response.json()

        # Parse and display current weather
        current_temperature = current_weather_data['main']['temp']
        current_weather_description = current_weather_data['weather'][0]['description']
        print(f"Current Weather in Kyiv:")
        print(f"Temperature: {current_temperature} K")
        print(f"Weather Description: {current_weather_description}")
    else:
        print("Error fetching current weather data.")

    # Fetch forecast data
    response = requests.get(forecast_url)
    if response.status_code == 200:
        forecast_data = response.json()

        # Parse and display forecast for the next 10 days
        forecast_list = forecast_data['list']
        print(f"\n10-day Weather Forecast for Kyiv:")
        for forecast in forecast_list[:10]:
            forecast_timestamp = forecast['dt']
            forecast_date = datetime.datetime.fromtimestamp(forecast_timestamp)
            forecast_temperature = forecast['main']['temp']
            forecast_weather_description = forecast['weather'][0]['description']
            print(f"Date: {forecast_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Temperature: {forecast_temperature} K")
            print(f"Weather Description: {forecast_weather_description}")
            print("---")
    else:
        print("Error fetching forecast data.")


if __name__ == "__main__":
    weather_in_kyiv()
