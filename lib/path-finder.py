'''
Calculate optimal route to empty glass containers. Units is in seconds. 

Google Maps API library from:
https://github.com/googlemaps/google-maps-services-python/blob/master/tests/test_distance_matrix.py
'''
import googlemaps
from preprocessing import read_data
from itertools import combinations
from datetime import datetime
import numpy as np
import os

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.replace('\n', '').split('='))
        for line in fh.readlines() if not line.startswith('#')
    )

sensor_data = read_data('data/fill-level.csv', use_coordinates=True)

gmaps = googlemaps.Client(key=vars_dict["MAPS_KEY"])

n = 10
dist_file = 'data/distances.npy'
time_per_working_day = 8 * 60 * 60 # 8 hours in seconds
time_per_emptying = 30 * 60 # 30 minutes in secnods
day = datetime(2023, 12, 4, 10, 00)

def get_distances(n):
    distances = np.empty((n,n))
    for (s_from, s_to) in combinations(range(n), 2):
        sensor_from = sensor_data.iloc[s_from]
        sensor_to = sensor_data.iloc[s_to]
        origins = [
            sensor_from["geo_point_2d"].split(",")
        ]
        destinations = [
            sensor_to["geo_point_2d"].split(",")
        ]

        matrix = gmaps.distance_matrix(
            origins, 
            destinations, 
            mode="driving", 
            language="de-CH",
            departure_time=day, # TODO: use specific date/time (also relevant for optimization)
            traffic_model="optimistic"
        )
        for row in matrix["rows"]:
            for element in row["elements"]:
                distance_in_seconds = element["duration"]["value"]

                # TODO: check if this makes sense:
                # Set weights of edges to inverse of level given by the sensor
                distances[s_from][s_to] = distance_in_seconds / sensor_to["level"]
                distances[s_to][s_from] = distance_in_seconds / sensor_from["level"]

    np.save(dist_file, distances)
    return distances

# distances matrix:  row=from, column=to
if os.path.isfile(dist_file):
    # Reuse distances to reduce api calls
    distances = np.load(dist_file)
else:
    distances = get_distances(n)

levels = [sensor_data.iloc[i]["level"] for i in range(n)]

print(distances)