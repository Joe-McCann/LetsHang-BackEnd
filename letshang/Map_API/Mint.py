from gmaps import GMaps
from graphFunctions import *
from mapPage import Map

gmap = GMaps('AIzaSyBCOPpz9nItjNrXMrTbA71B0pCX2o5P1E8')
page = Map()
address_list = ['9 Appletree Drive, Matawan, NJ',
                '23 Boxwood Circle, Edison, NJ']

address_coords = [gmap.address_to_longlat(x) for x in address_list]
reccomendations = [centroid(address_coords),
                    geoMean(address_coords, .001, 10000),
                    minSig(address_coords, .001, 100000)]

for point in address_coords:
    page.add_point(point)

page.add_point(reccomendations[0], color='42F4D4')
page.add_point(reccomendations[1], color='DA36E2')
page.add_point(reccomendations[2], color='3AED0E')

with open("output.html", "w") as out:
    print(page, file=out)
                   
