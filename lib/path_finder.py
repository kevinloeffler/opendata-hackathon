'''
Calculate optimal route to empty glass containers. Units are in seconds. 
'''
from preprocessing import read_data
from map_service import MapService
import numpy as np
from datetime import datetime
import os

create_map = True
show_min_max_markers = False
dist_file = 'data/distances.npy'
time_per_working_day = 8 * 60 * 60 # 8 hours in seconds
time_per_emptying = 30 * 60 # 15 minutes in seconds
day = datetime(2023, 12, 4, 10, 00) # Date of prediction
station_0 = (47.4156038, 9.3325804) # Assumption: Empyting starts and ends at Kehrichtheizkraftwerk St.Gallen
empty_if_below = 0.4

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.replace('\n', '').split('='))
        for line in fh.readlines() if not line.startswith('#')
    )

sensor_data = read_data('data/fill-level.csv', use_coordinates=True)
sensor_data = sensor_data.loc[sensor_data.groupby('sensor_id').date.idxmax()] # Get sensor_id only once
#sensor_data = sensor_data[sensor_data['level'] > empty_if_below-0.1] # Don't use very low values to get more interesting results

n = sensor_data.shape[0] if sensor_data.shape[0] < 50 else 50 # Take a look at the n highest sensor levels of the next day

map_service = MapService(vars_dict["MAPS_KEY"], sensor_data, day, n, station_0, empty_if_below)

# distances matrix: row=from, column=to
if os.path.isfile(dist_file):
    # Reuse distances to reduce api calls
    distances = np.load(dist_file)
else:
    distances = map_service.get_distances()
    np.save(dist_file, distances)

levels = [sensor_data.iloc[i]["level"] for i in range(n)]

needed_time = 0
current_stop_idx = -1 #station_0 index
visited_stops = []

# distances[current_stop_idx, 0] is the time needed from the station to station_0
while (needed_time < (time_per_working_day - distances[current_stop_idx, -1] - time_per_emptying)):
    visited_stops.append(current_stop_idx)

    if len(visited_stops) == n+1:
        # all stops visited
        break
    min_cost = np.min(np.delete(distances[current_stop_idx,:], visited_stops, axis=0)) # Min cost of unvisited stops
    for idx in np.argwhere(distances[current_stop_idx,:] == min_cost).ravel():
        if idx not in visited_stops:
            next_stop_idx = idx
    
    actual_travel_time = sensor_data.iloc[next_stop_idx]["level"]
    needed_time += actual_travel_time + time_per_emptying
    current_stop_idx = next_stop_idx

visited_stops.append(-1) # End at station_0
needed_time += distances[current_stop_idx, -1] # Add time to go to station_0
    
print("Needed time:")
print(needed_time)
print("Trajectory:")
for stop in visited_stops:
    if stop != -1:
        print(f"{stop} -> {levels[stop]}")

unvisited_stops = np.setdiff1d(range(n), visited_stops)
print("Unvisited:")
print(unvisited_stops)
print("Filling levels:")
print(levels)

if create_map:
    map_response = map_service.generate_map(visited_stops, show_min_max_markers)
    f = open("map-output.png", 'wb')
    for chunk in map_response:
        if chunk:
            f.write(chunk)
    f.close()
