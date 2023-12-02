'''
Calculate optimal route to empty glass containers. Units are in seconds. 
'''
from preprocessing import read_data
from map_service import MapService
import numpy as np
import pandas as pd
import os

create_map = True
show_min_max_markers = False
data_file = 'data/days_merged.csv'
dist_file = 'data/distances.npy'
map_file = 'map-output.png'
map_file_refined = 'map-output-refined.png'

class PathFinder:
    capacity = 5.5 - 1 # size of trough minus 1 container
    time_per_working_day = 6 * 60 * 60 # 6 hours in seconds divided by 3 because only 40/120 containers have sensors
    time_per_emptying = 15 * 60 # 15 minutes in seconds, 5 minutes per container

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

        needed_capacity = 0
        needed_time = 0
        current_stop_idx = -1 #station_0 index
        visited_stops = [current_stop_idx]
        visited_locations = [self.station_0]

        # distances[current_stop_idx, 0] is the time needed from the station to station_0
        while (needed_time < (self.time_per_working_day - cost_matrix[current_stop_idx, -1] - self.time_per_emptying) and needed_capacity < self.capacity):
            if len(visited_stops) == self.n_sensors+1:
                # all stops visited
                break

            min_cost = np.min(np.delete(cost_matrix[current_stop_idx,:], visited_stops, axis=0)) # Min cost of unvisited stops
            for idx in np.argwhere(cost_matrix[current_stop_idx,:] == min_cost).ravel():
                if idx not in visited_stops:
                    next_stop_idx = int(idx)
            
            needed_capacity += self.sensor_data.iloc[next_stop_idx]["level"]
            actual_travel_time = self.dist_matrix[current_stop_idx][next_stop_idx]
            needed_time += actual_travel_time + self.time_per_emptying
            current_stop_idx = next_stop_idx
            visited_stops.append(next_stop_idx)
            location_information = {}
            location_information["lat"] = self.sensor_data.iloc[next_stop_idx]["geo_point_2d"].split(", ")[0]
            location_information["lng"] = self.sensor_data.iloc[next_stop_idx]["geo_point_2d"].split(", ")[1]
            location_information["level"] = self.sensor_data.iloc[next_stop_idx]["level"]
            location_information["sensor_id"] = self.sensor_data.iloc[next_stop_idx]["sensor_id"]
            location_information["date"] = self.sensor_data.iloc[next_stop_idx]["date"]
            location_information["type"] = self.sensor_data.iloc[next_stop_idx]["type"].split(", ")[0]

            visited_locations.append(location_information)

        visited_stops.append(-1) # End at station_0
        visited_locations.append(self.station_0)
        needed_time += cost_matrix[current_stop_idx, -1] # Add time to go to station_0

        return visited_stops, needed_time, visited_locations, needed_capacity

    def refine_path(self, starting_point_idx, visited_stops):
        # refine path using dijkstra
        unvisited = visited_stops[1:-1]
        tour = [visited_stops[starting_point_idx]] # Start from the first point
        unvisited.remove(tour[-1])
        locations = [self.sensor_data.iloc[tour[-1]]["geo_point_2d"].split(", ")]

        while unvisited:
            current_point = tour[-1]
            min_dist = np.min(self.dist_matrix[current_point][unvisited])
            for idx in np.argwhere(self.dist_matrix[current_point] == min_dist).ravel():
                if idx in unvisited:
                    nearest_point = int(idx)
            tour.append(nearest_point)
            locations.append(self.sensor_data.iloc[nearest_point]["geo_point_2d"].split(", "))
            unvisited.remove(nearest_point)

        return tour, locations

if __name__ == "__main__":
    with open('.env', 'r') as fh:
        vars_dict = dict(
            tuple(line.replace('\n', '').split('='))
            for line in fh.readlines() if not line.startswith('#')
        )
    
    n_sensors = 42 # Number of sensors in St. Gallen
    no_empty_if_below = 0.4
    station_0 = (47.4156038, 9.3325804) # Assumption: Empyting starts and ends at Kehrichtheizkraftwerk St.Gallen
    columns = [
        'sensor_id','date','geo_point_2d','level','type'
    ]
    sensor_data = pd.read_csv(data_file, delimiter=',', usecols=columns)
    sensor_data = sensor_data.loc[sensor_data.groupby('sensor_id').date.idxmax()] # Get sensor_id only once

    map_service = MapService(vars_dict["MAPS_KEY"], sensor_data, n_sensors, station_0, no_empty_if_below)
    path_finder = PathFinder(map_service, sensor_data, station_0, n_sensors)

    levels = [sensor_data.iloc[i]["level"] for i in range(n_sensors)]

    visited_stops, needed_time, visited_locations, needed_capacity = path_finder.find_path()
    
    print("Needed time:", needed_time)
    print("Needed capacity:", needed_capacity)
    print("Path:")
    for stop in visited_stops:
        if stop != -1:
            print(f"{stop} -> {levels[stop]}")

    unvisited_stops = np.setdiff1d(range(n_sensors), visited_stops)
    print("Unvisited Sensors:")
    print(unvisited_stops)

    if create_map:
        map_response = map_service.generate_map(visited_locations, show_min_max_markers)
        f = open(map_file, 'wb')
        for chunk in map_response:
            if chunk:
                f.write(chunk)
        f.close()

    most_left_point = np.argmin([float(x["lat"]) for x in visited_locations[1:-1]])
    tour, locations = path_finder.refine_path(most_left_point, visited_stops)
    locations = [station_0] + locations + [station_0]

    print("Refined path", tour)
    if create_map:
        map_response = map_service.generate_map(locations, show_min_max_markers)
        f = open(map_file_refined, 'wb')
        for chunk in map_response:
            if chunk:
                f.write(chunk)
        f.close()