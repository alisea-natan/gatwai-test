import click
import requests


def get_weather(city_name, api_key):
    # Current weather API endpoint
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    # Fetch current weather
    response = requests.get(current_weather_url)
    if response.status_code == 200:
        current_weather_data = response.json()

        # Parse and display current weather
        temperature = current_weather_data['main']['temp']
        weather_description = current_weather_data['weather'][0]['description']
        click.echo(f"Weather in {city_name}:")
        click.echo(f"Temperature: {temperature} K")
        click.echo(f"Weather Description: {weather_description}")
    else:
        click.echo("Error fetching weather data.")


@click.command()
@click.argument('city')
@click.option('--api-key', help='OpenWeatherMap API key', required=True)
def main(city, api_key):
    get_weather(city, api_key)


if __name__ == '__main__':
    main()
