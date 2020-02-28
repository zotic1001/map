import requests
import sys


def delta_find(toponym_to_find, geocoder_params, geocoder_api_server):
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json = response.json()
    toponym = json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    ng = toponym["boundedBy"]["Envelope"]["lowerCorner"]
    vg = toponym["boundedBy"]["Envelope"]["upperCorner"]
    xd = abs(float(ng.split()[0]) - float(vg.split()[0])) / 2
    yd = abs(float(ng.split()[1]) - float(vg.split()[1])) / 2
    return xd, yd
