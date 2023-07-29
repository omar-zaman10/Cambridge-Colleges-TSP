import pandas as pd
import googlemaps
from pprint import pprint
from config import key,colleges


if key == 'YOUR_GOOGLE_MAPS_API_KEY_HERE': raise ValueError('API key is not entered in .env file')


gmaps = googlemaps.Client(key=key)

table = pd.DataFrame({'College' : colleges})

geocodes = pd.read_csv('Data/Geocodes.csv')

geo_list = []

for college in colleges:
    code = geocodes[college]
    geo_list.append([code[0],code[1]])



for college in colleges:

    g1 = geocodes[college]

    distance1 = gmaps.distance_matrix([[g1[0],g1[1]]],geo_list[:15],mode ='bicycling')
    distance2 = gmaps.distance_matrix([[g1[0],g1[1]]],geo_list[15:],mode ='bicycling')

    distances = distance1['rows'][0]['elements']
    my_list = []

    for d in distances:
        my_list.append(d['distance']['value'])
    
    distances = distance2['rows'][0]['elements']

    for d in distances:
        my_list.append(d['distance']['value'])

    table[college] = my_list

 

pprint(table)

table.to_csv('Data/Distances_table.csv')

