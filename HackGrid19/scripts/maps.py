# Enter your api key here
api_key = "AIzaSyA8PkLtaTkbHERnjJeU7AHe3_NeuuYhLnE"

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key=api_key)

def get_geolocations(city,country):
    geocode_result = gmaps.geocode(city+" , "+country)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    return [lat,lon]
