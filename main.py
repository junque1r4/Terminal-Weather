import string
import argparse
from rich.console import Console
from rich import print as prnt
import json
from urllib import parse, request, error
import sys
from API_KEY import API_KEY as KEY # Put your API key in the in a python file with a constant named API_KEY 

BASE_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
console = Console()


def read_user_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = 'Get weather and temperature information for a city!'
    )

    parser.add_argument(
        "city", nargs = '+', type = str, help = 'Enter the name of the city.'
    )

    return parser.parse_args()

def weather_query(city) -> string:
    city_name = ' '.join(city)
    url_encoded_city_name = parse.quote_plus(city_name)

    url = (
        f'{BASE_API_URL}?q={url_encoded_city_name}&units=metric&APPID={KEY}'
    )

    return url

def get_weather_data(query_url) -> dict:
    with console.status('[bold green]Loading data...', spinner='earth'):
        try:
            response = request.urlopen(query_url)
        except error.HTTPError as http_error:
            if http_error.code == 404:
                sys.exit("Can't find weather data for this place.")
            elif http_error.code == 401:
                sys.exit('Access denied. Check your API key.')
            else:
                sys.exit(f'Something went wrong... error code: {http_error.code}')
    data = response.read()
    
    try:
        return json.loads(data)
    except:
        sys.exit('Couldnt convert data into JSON.')

def show_weather_data(data_in_json) -> None:
    city = data_in_json['name']
    description = data_in_json["weather"][0]["description"]
    temperature = data_in_json["main"]["temp"]
    wind_speed = data_in_json['wind']['speed']

    prnt(f'[bold white]:heavy_check_mark:[bold yellow] {city}', end=' ')
    prnt(f':cloud:[bold white] {description.capitalize()}', end=' ')
    prnt(f':thermometer:[bold cyan] {temperature}°C', end=' ')
    prnt(f':dash:[bold green] {wind_speed}Km/h')

if __name__ == '__main__':
    user_args = read_user_args()
    query_url = weather_query(user_args.city)
    weather_data = get_weather_data(query_url)
    show_weather_data(weather_data)

"""              TODOLIST            """
# TODO: Implement some parsing for the user output, security first!
# TODO: Emoticon change deppending on the description
# TODO: Temperature color change deppending on the temperature
# TODO: Build executable zip application with zipapp
# TODO: Put some color in the error handling
# TODO: Put some color in the -h --help
