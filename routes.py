import pandas as pd
import polyline
import folium


def tsp_cycle(map,perm):


    for i in range(-1,len(perm)-1):
        origin = perm[i]
        destination = perm[i+1]
        route = data[origin + ',' + destination]

        directions = []

        for p in route:
            if pd.isna(p) : break
            line = polyline.decode(p)
            directions.append(line)

        folium.PolyLine(directions, weight=5, opacity=1).add_to(map)


if __name__ == '__main__':

    data = pd.read_csv('Data/Directions.csv')
    geocodes = pd.read_csv('Data/Geocodes.csv')


    alternate_route = ['Darwin College Cambridge', 'Queens College Cambridge', 'Corpus Christi College Cambridge', 
    'Emmanuel College Cambridge', 'Hughes Hall Cambridge', 'Homerton College Cambridge', 'Downing College Cambridge','Peterhouse Cambridge',
    'Pembroke College Cambridge','St Catharines College Cambridge', 'Kings College Cambridge', 
    'Gonville and Caius College Cambridge', 'Clare College Cambridge', 'Trinity Hall Cambridge', 'Trinity College Great Court Cambridge', 
    'Christs College Cambridge', 'Sidney Sussex College Cambridge', 'Jesus College Cambridge', 'St Johns College Cambridge',
    'Magdalene College Cambridge', 'Lucy Cavendish College Cambridge','St Edmunds College Cambridge', 'Murray Edwards College Cambridge', 'Girton College Cambridge', 
    'Fitzwilliam College Cambridge', 'Churchill College Cambridge', 'Robinson College Cambridge', 
    'Clare Hall Cambridge', 'Selwyn College Cambridge', 'Wolfson College Cambridge', 'Newnham College Cambridge']

    best_route = ['Queens College Cambridge', 'Darwin College Cambridge', 'Newnham College Cambridge', 'Wolfson College Cambridge',
                'Selwyn College Cambridge', 'Clare Hall Cambridge', 'Robinson College Cambridge', 'St Johns College Cambridge',
                'Lucy Cavendish College Cambridge', 'St Edmunds College Cambridge', 'Murray Edwards College Cambridge',
                    'Girton College Cambridge', 'Fitzwilliam College Cambridge', 'Churchill College Cambridge',
                    'Magdalene College Cambridge', 'Trinity College Great Court Cambridge', 'Trinity Hall Cambridge',
                        'Clare College Cambridge', 'Kings College Cambridge', 'Gonville and Caius College Cambridge',
                        'Jesus College Cambridge', 'Sidney Sussex College Cambridge', 'Christs College Cambridge',
                            'Emmanuel College Cambridge', 'Hughes Hall Cambridge', 'Homerton College Cambridge',
                            'Downing College Cambridge', 'Peterhouse Cambridge', 'Pembroke College Cambridge', 
                            'Corpus Christi College Cambridge', 'St Catharines College Cambridge']

    map1=folium.Map(location=[52.2069577, 0.1130816],zoom_start=13.5) 
    map2=folium.Map(location=[52.2069577, 0.1130816],zoom_start=13.5) 


    
    for college in geocodes:

        lat,lng = geocodes[college]

        map1.add_child(folium.Marker(location=[lat, lng],popup=college,icon=folium.Icon(color='red')))
        map2.add_child(folium.Marker(location=[lat, lng],popup=college,icon=folium.Icon(color='green')))



    tsp_cycle(map1,best_route)
    tsp_cycle(map2,alternate_route)

    map1.save("Maps/best_route.html")
    map2.save("Maps/alternate_route.html")