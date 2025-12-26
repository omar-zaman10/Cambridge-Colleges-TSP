import folium
import pandas as pd

if __name__ == '__main__':

    # Map centred from trinity lat long
    map=folium.Map(location=[52.2069577, 0.1130816],zoom_start=13.5) 

    geocodes = pd.read_csv('Data/Geocodes.csv')

    for college in geocodes:
        lat,lng = geocodes[college]
        map.add_child(folium.Marker(location=[lat, lng],popup=college,icon=folium.Icon(color='red')))


    map.save("maps/colleges_map.html")