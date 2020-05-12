import json
import os
import requests

from flask import Flask, render_template, request


app = Flask(__name__)
app.config['OPENWEATHERMAP_API_KEY'] = os.environ.get('OPENWEATHERMAP_API_KEY')
app.config['IPSTACK_API_KEY'] = os.environ.get('IPSTACK_API_KEY')

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


def get_response_dict(url):
    response = requests.get(url)
    response_dict = json.loads(response.text)
    return response_dict


def get_location_dict(ip_addr):
    # ip_addr = '8.8.8.8'
    base_url = 'http://api.ipstack.com/'
    full_url = f'{base_url}{ip_addr}?access_key={app.config["IPSTACK_API_KEY"]}'
    return get_response_dict(full_url)


def get_weather_dict(latitude, longitude):
    # latitude = 35 
    # longitude = 139
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = (
        f'appid={app.config["OPENWEATHERMAP_API_KEY"]}'
        f'&lat={latitude}'
        f'&lon={longitude}'
        '&units=imperial'
    )
    full_url = f'{base_url}?{parameters}'
    return get_response_dict(full_url)


# @app.route('/')
def test():
    nice_out_key = 'Yes'
    location_dict = 'TEST TEST TEST'
    return render_template('index.html', nice_out=nice_out_dict[nice_out_key], location_dict=location_dict)


@app.route('/')
@app.route('/isitniceout')
def isitniceout():
    '''
    Use ipstack and openweathermap APIs
    to determine whether it's nice out.
    '''

    # This does not work locally because localhost does not have geoip data
    ip_addr = request.access_route[-1] 
    # ip_addr = '8.8.8.8'
    location_dict = get_location_dict(ip_addr=ip_addr)

    latitude = location_dict['latitude']
    longitude = location_dict['longitude']
    weather_dict = get_weather_dict(latitude=latitude, longitude=longitude)

    feels_like = weather_dict['main']['feels_like']
    wind_speed = weather_dict['wind']['speed']
    precipitation = ('rain' in weather_dict or 'snow' in weather_dict)

    nice_out_key = 'No'
    if ((feels_like >= 60 and feels_like <= 82) and
        (wind_speed < 10) and
        (not precipitation)):
       nice_out_key = 'Yes'

    detail_dict = {
        'ip_addr': ip_addr,
        'latitude': latitude,
        'longitude': longitude,
        'feels_like': feels_like,
        'wind_speed': wind_speed,
        'precipitation': precipitation
    }

    return render_template('index.html', nice_out=nice_out_dict[nice_out_key], detail_dict=detail_dict)