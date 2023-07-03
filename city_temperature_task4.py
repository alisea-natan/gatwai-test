import os

import click
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API")


def get_weather(city_name, api_key):
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    response = requests.get(current_weather_url)
    if response.status_code == 200:
        current_weather_data = response.json()

        temperature = current_weather_data['main']['temp']
        weather_description = current_weather_data['weather'][0]['description']
        click.echo(f"Weather in {city_name}:")
        click.echo(f"Temperature: {temperature} K")
        click.echo(f"Weather Description: {weather_description}")
    else:
        click.echo("Error fetching weather data. Check your API key and internet connection.")


@click.command()
@click.argument('city')
@click.option('--api-key', help='OpenWeatherMap API key', required=True, default=API_KEY)
def main(city, api_key):
    get_weather(city, api_key)


if __name__ == '__main__':
    main()
