import json
import os
import requests

from flask_simple_geoip import SimpleGeoIP
from flask import Flask, render_template


app = Flask(__name__)
app.config['OPENWEATHERMAP_API_KEY'] = os.environ.get('OPENWEATHERMAP_API_KEY')
app.config['GEOIPIFY_API_KEY'] = os.environ.get('GEOIPIFY_API_KEY')

simple_geoip = SimpleGeoIP(app)

nice_out_dict = {
    'Yes': {
        'value': 'Yes',
        'text_color': '#f0eec9',
        'background_color': '#7aed70'
    },
    'No': {
        'value': 'No',
        'text_color': '#6a6475',
        'background_color': '#ff798b'
    }
}


# @app.route('/')
def test():
    nice_out_key = 'Yes'
    location_dict = 'TEST TEST TEST'
    return render_template('index.html', nice_out=nice_out_dict[nice_out_key], location_dict=location_dict)


@app.route('/')
@app.route('/isitniceout')
def isitniceout():
    '''
    Use openweathermap API (https://openweathermap.org/current)
    to determine whether it's nice out.
    '''
    location_dict = simple_geoip.get_geoip_data()['location']

    # location_id = 5110302
    # lat = 35 & lon = 139
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = (
        f'appid={app.config["OPENWEATHERMAP_API_KEY"]}'
        f'&lat={location_dict["lat"]}'
        f'&lon={location_dict["lng"]}'
        '&units=imperial'
    )

    response = requests.get(f'{base_url}?{parameters}')
    response_dict = json.loads(response.text)

    feels_like = response_dict['main']['feels_like']
    wind_speed = response_dict['wind']['speed']
    precipitation = ('rain' in response_dict or 'snow' in response_dict)

    nice_out_key = 'No'
    if ((feels_like >= 60 and feels_like <= 82) and
        (wind_speed < 10) and
        (not precipitation)):
       nice_out_key = 'Yes'

    return render_template('index.html', nice_out=nice_out_dict[nice_out_key], location_dict=location_dict)