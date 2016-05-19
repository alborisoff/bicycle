# -*- Coding: UTF-8 -*-

import json
import io


# Reformating input JSON to GeoJSON
def jsontogeo(inputjson):

    dictprops = {}  # Dictionary for parking properties
    onepark_dict = {}  # Dictionary for one parking
    pos_dict = {}  # Object position dictionary
    arrparks = []  # Array of all parks
    ready_dict = {}  # Ready JSON
    jsone_data = open(inputjson).read()
    jsone = json.loads(jsone_data)
    for oneparking in jsone['Items']:
        dictprops['Id'] = oneparking['Id']
        dictprops['IsLocked'] = oneparking['IsLocked']
        dictprops['Address'] = oneparking['Address']
        dictprops['FreePlaces'] = oneparking['FreePlaces']
        dictprops['TotalPlaces'] = oneparking['TotalPlaces']
        pos_lat = oneparking['Position']['Lat']
        pos_lon = oneparking['Position']['Lon']
        onepark_dict['type'] = 'Feature'
        pos_dict['type'] = 'Point'
        pos_dict['coordinates'] = [pos_lon, pos_lat]
        onepark_dict['geometry'] = pos_dict
        onepark_dict['properties'] = dictprops
        arrparks.append(onepark_dict)
        onepark_dict = {}
        pos_dict = {}
        dictprops = {}
    ready_dict['type'] = 'FeatureCollection'
    ready_dict['features'] = arrparks
    return ready_dict
        

togeojson = jsontogeo('Parkings.json')
# Saving ready GeoJSON
with io.open('velopark.geojson', 'w', encoding='utf-8') as readygeojson:
    readygeojson.write(unicode(json.dumps(togeojson, ensure_ascii=False)))
