import googlemaps
from pprint import pprint
import pandas as pd
from config import key,colleges

if key == 'YOUR_GOOGLE_MAPS_API_KEY_HERE': raise ValueError('API key is not entered in .env file')


gmaps = googlemaps.Client(key=key)

geocodes = pd.read_csv('Data/Geocodes.csv')

data = {}

for origin in colleges:
    for destination in colleges:
        title = origin + ',' + destination

        data[title] = []

        g1 = geocodes[origin]
        g2 = geocodes[destination]

        response = gmaps.directions(g1,g2,mode='walking')

        steps = response[0]['legs'][0]['steps']


        for step in steps:
            p= step['polyline']['points']
            data[title].append(p)


max_length = len(max(data.values(),key = lambda x: len(x)))

#Making every column have the same number of entries by appengin Null values
for key,value in data.items():
    value += [None]*(max_length-len(value))

    data[key] = value



data = pd.DataFrame(data)
pprint(data)


data.to_csv('Data/Directions.csv')
