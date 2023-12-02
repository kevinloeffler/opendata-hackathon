'''
Calculate optimal route to empty glass containers. Units are in seconds. 
'''
from preprocessing import read_data
from map_service import MapService
import numpy as np
import pandas as pd
from datetime import datetime
import os

create_map = True
show_min_max_markers = False
data_file = 'data/fill-level.csv'
dist_file = 'data/distances.npy'
map_file = 'map-output.png'

class PathFinder:
    time_per_working_day = 8 * 60 * 60 # 8 hours in seconds
    time_per_emptying = 30 * 60 # 15 minutes in seconds

    def __init__(self,  map_service: MapService, sensor_data: pd.DataFrame, station_0: tuple, n_sensors: int):
        self.sensor_data = sensor_data
        self.station_0 = station_0
        self.map_service = map_service
        self.n_sensors = n_sensors
        
        # distances matrix: row=from, column=to
        if os.path.isfile(dist_file):
            # Reuse distances to reduce api calls
            self.dist_matrix = np.load(dist_file)
        else:
            self.dist_matrix = self.map_service.get_distances()
            np.save(dist_file, self.dist_matrix)

    def find_path(self):
        cost_matrix = self.map_service.get_costs(self.dist_matrix)

        needed_time = 0
        current_stop_idx = -1 #station_0 index
        visited_stops = []

        # distances[current_stop_idx, 0] is the time needed from the station to station_0
        while (needed_time < (self.time_per_working_day - cost_matrix[current_stop_idx, -1] - self.time_per_emptying)):
            visited_stops.append(current_stop_idx)

            if len(visited_stops) == self.n_sensors+1:
                # all stops visited
                break
            min_cost = np.min(np.delete(cost_matrix[current_stop_idx,:], visited_stops, axis=0)) # Min cost of unvisited stops
            for idx in np.argwhere(cost_matrix[current_stop_idx,:] == min_cost).ravel():
                if idx not in visited_stops:
                    next_stop_idx = idx
            
            actual_travel_time = self.sensor_data.iloc[next_stop_idx]["level"]
            needed_time += actual_travel_time + self.time_per_emptying
            current_stop_idx = next_stop_idx

        visited_stops.append(-1) # End at station_0
        needed_time += cost_matrix[current_stop_idx, -1] # Add time to go to station_0

        return visited_stops, needed_time

if __name__ == "__main__":
    with open('.env', 'r') as fh:
        vars_dict = dict(
            tuple(line.replace('\n', '').split('='))
            for line in fh.readlines() if not line.startswith('#')
        )
    
    day = datetime(2023, 12, 4, 10, 00) # Date of prediction
    n_sensors = 42 # Number of sensors in St. Gallen
    no_empty_if_below = 0.4
    station_0 = (47.4156038, 9.3325804) # Assumption: Empyting starts and ends at Kehrichtheizkraftwerk St.Gallen
    sensor_data = read_data(data_file, use_coordinates=True)
    sensor_data = sensor_data.loc[sensor_data.groupby('sensor_id').date.idxmax()] # Get sensor_id only once

    map_service = MapService(vars_dict["MAPS_KEY"], sensor_data, day, n_sensors, station_0, no_empty_if_below)
    path_finder = PathFinder(map_service, sensor_data, station_0, n_sensors)

    levels = [sensor_data.iloc[i]["level"] for i in range(n_sensors)]

    visited_stops, needed_time = path_finder.find_path()
    
    print("Needed time:", needed_time)
    print("Path:")
    for stop in visited_stops:
        if stop != -1:
            print(f"{stop} -> {levels[stop]}")

    unvisited_stops = np.setdiff1d(range(n_sensors), visited_stops)
    print("Unvisited Sensors:")
    print(unvisited_stops)

    if create_map:
        map_response = map_service.generate_map(visited_stops, show_min_max_markers)
        f = open(map_file, 'wb')
        for chunk in map_response:
            if chunk:
                f.write(chunk)
        f.close()
