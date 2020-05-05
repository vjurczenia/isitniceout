"""
Updated the windspeed and temperature limits
Also added a geolocation pulled from the user's IP.
"""

import json
import os
import requests

from flask_simple_geoip import SimpleGeoIP
from flask import Flask, render_template, jsonify


app = Flask(__name__)
OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')
app.config["GEOIPIFY_API_KEY"] = os.environ.get('GEOIPIFY_API_KEY')

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

def user_loc():
    # Retrieve geoip data for the given requester
    geoip_data = simple_geoip.get_geoip_data()
    return jsonify(data=geoip_data)


#@app.route('/')
def test():
    nice_out_key = 'No'
    return render_template('index.html', nice_out=nice_out_dict[nice_out_key])


@app.route('/')
@app.route('/isitniceout')
def isitniceout():
    """
    Use openweathermap API (https://openweathermap.org/current)
    to determine whether it's nice out.
    """
    location_dict = user_loc()

    #location_id = 5110302
    # lat = 35 & lon = 139
    base_url = 'api.openweathermap.org/data/2.5/weather'
    parameters = (
        f'appid={OPENWEATHERMAP_API_KEY}'
        f'&lat={location_dict["lat"]}'
        f'&lon={location_dict["lng"]}'
        '&units=imperial'
    )

    response = requests.get(f"{base_url}?{parameters}")
    response_dict = json.loads(response.text)

    feels_like = response_dict['main']['feels_like']
    wind_speed = response_dict['wind']['speed']
    precipitation = ('rain' in response_dict or 'snow' in response_dict)

    nice_out_key = 'No'
    if ((feels_like >= 60 and feels_like <= 82) and
        (wind_speed < 10) and
        (not precipitation)):
       nice_out_key = 'Yes'

    return render_template('index.html', nice_out=nice_out_dict[nice_out_key])