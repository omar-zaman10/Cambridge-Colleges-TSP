import googlemaps
from pprint import pprint
import pandas as pd
from config import key , colleges


if key == 'YOUR_GOOGLE_MAPS_API_KEY_HERE': raise ValueError('API key is not entered in .env file')

gmaps = googlemaps.Client(key=key)

table = pd.DataFrame({'College' : colleges})

geocodes = pd.DataFrame()


for college in colleges:

    geocode = gmaps.geocode(college)
    geocode = geocode[0]['geometry']['location']

    geocodes[college] = (geocode['lat'],geocode['lng'])

geocodes.to_csv('Data/Geocodes.csv')

pprint(geocodes)