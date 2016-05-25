# Coding: UTF-8

import json
import io
import psycopg2


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
pre_togeojson_utf = unicode(json.dumps(togeojson, ensure_ascii=False))
togeojson_utf = json.loads(pre_togeojson_utf)
# print pre_togeojson_utf
print togeojson_utf

# Saving ready GeoJSON
with io.open('velopark.geojson', 'w', encoding='utf-8') as readygeojson:
    readygeojson.write(unicode(json.dumps(togeojson, ensure_ascii=False)))

connection_config = "dbname = 'postgres' user = 'postgres' host = 'localhost' password = 'postgres'"
velo_connect = psycopg2.connect(connection_config)
velo_cursor = velo_connect.cursor()
for onepark in togeojson_utf['features']:
    v_pgsql_id = onepark['properties']['Id']
    v_pgsql_address = onepark['properties']['Address']
    v_pgsql_islocked = onepark['properties']['IsLocked']
    v_pgsql_totalplaces = onepark['properties']['TotalPlaces']
    v_pgsql_freeplaces = onepark['properties']['FreePlaces']
    v_pgsql_lat = onepark['geometry']['coordinates'][1]
    v_pgsql_lon = onepark['geometry']['coordinates'][0]

    v_query = 'INSERT INTO velobikes2 (id, address, islocked, totalplaces, freeplaces, lat, lon) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s)'
    v_data = (v_pgsql_id, v_pgsql_address, v_pgsql_islocked, v_pgsql_totalplaces, v_pgsql_freeplaces, v_pgsql_lat,
              v_pgsql_lon)
    velo_cursor.execute(v_query, v_data)
velo_connect.commit()
