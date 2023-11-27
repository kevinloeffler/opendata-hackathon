import googlemaps
from datetime import datetime

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.replace('\n', '').split('='))
        for line in fh.readlines() if not line.startswith('#')
    )

gmaps = googlemaps.Client(key=vars_dict["MAPS_KEY"])

origins = [
    (47.4120960807, 9.3359106884)
]
destinations = [
    (47.43724, 9.37681),
]

matrix = gmaps.distance_matrix(origins, destinations)
for row in matrix["rows"]:
    for element in row["elements"]:
        print(element["duration"])
print(matrix)