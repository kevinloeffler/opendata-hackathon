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

dist_file = 'data/distances.npy'
n = 10 # Take a look at the n highest sensor levels of the next day
time_per_working_day = 8 * 60 * 60 # 8 hours in seconds
time_per_emptying = 30 * 60 # 30 minutes in seconds
day = datetime(2023, 12, 4, 10, 00) # Date of prediction
station_0 = (47.4156038, 9.3325804) # Assumption: Empyting starts and ends at Kehrichtheizkraftwerk St.Gallen

def get_distances(n):
    distances = np.empty((n+1,n+1))
    for (node_from, node_to) in combinations(range(n), 2):
        sensor_from = sensor_data.iloc[node_from]
        sensor_to = sensor_data.iloc[node_to]
        origins = [
            sensor_from["geo_point_2d"].split(", ")
        ]
        destinations = [
            sensor_to["geo_point_2d"].split(", ")
        ]

        matrix = gmaps.distance_matrix(
            origins, 
            destinations, 
            mode="driving", 
            language="de-CH",
            departure_time=day, # TODO: use specific date/time (also relevant for optimization)
            traffic_model="optimistic"
        )
        distance_in_seconds = matrix["rows"][0]["elements"][0]["duration"]["value"]

        # TODO: check if this makes sense:
        # Set weights of edges to inverse of level given by the sensor
        distances[node_from+1][node_to+1] = distance_in_seconds / sensor_to["level"]
        distances[node_to+1][node_from+1] = distance_in_seconds / sensor_from["level"]

    for node_to in range(n):
        sensor_to = sensor_data.iloc[node_to]
        origins = [
            station_0
        ]
        destinations = [
            sensor_to["geo_point_2d"].split(",")
        ]

        matrix = gmaps.distance_matrix(
            origins, 
            destinations, 
            mode="driving", 
            language="de-CH",
            departure_time=day.replace(hour=17), # We go home at 17:00 :)
            traffic_model="optimistic"
        )
        distance_in_seconds = matrix["rows"][0]["elements"][0]["duration"]["value"]

        # TODO: check if this makes sense:
        # Set weights of edges to inverse of level given by the sensor
        distances[0][node_to+1] = distance_in_seconds / sensor_to["level"]
        distances[node_to+1][0] = distance_in_seconds

    np.save(dist_file, distances)
    return distances

# distances matrix: row=from, column=to
if os.path.isfile(dist_file):
    # Reuse distances to reduce api calls
    distances = np.load(dist_file)
else:
    distances = get_distances(n)

levels = [sensor_data.iloc[i]["level"] for i in range(n)]

print(distances)

# TODO: always take nearest node and add it to the graph while needed_time < time_per_working_day
# TODO: add daily weights if nodes have not been processed today