import json
import os
import requests

from flask import Flask


app = Flask(__name__)
OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')


@app.route('/')
@app.route('/isitniceout')
def isitniceout():
    """
    Use openweathermap API (https://openweathermap.org/current)
    to determine whether it's nice out.
    """
    location_id = 5110302

    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = (
        f'appid={OPENWEATHERMAP_API_KEY}'
        f'&id={location_id}'
        '&units=imperial'
    )

    response = requests.get(f"{base_url}?{parameters}")
    response_dict = json.loads(response.text)

    feels_like = response_dict['main']['feels_like']
    wind_speed = response_dict['wind']['speed']
    precipitation = ('rain' in response_dict or 'snow' in response_dict)

    if ((feels_like >= 40 and feels_like <= 82) and 
        (wind_speed < 15) and
        (not precipitation)):
       return 'Yes'

    return 'No'