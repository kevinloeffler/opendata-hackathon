'''
Google Maps API library from:
https://github.com/googlemaps/google-maps-services-python/blob/master/tests/test_distance_matrix.py
'''
import googlemaps
import pandas as pd
import numpy as np
from datetime import datetime
from itertools import combinations
from googlemaps.maps import StaticMapPath
from googlemaps.maps import StaticMapMarker


class MapService:
    def __init__(self, key: str, sensor_data: pd.DataFrame, day: datetime, n_sensors: int, station_0: tuple, no_empty_if_below: float):
        self.gmaps = googlemaps.Client(key=key)
        self.sensor_data = sensor_data
        self.day = day
        self.n_sensors = n_sensors
        self.station_0 = station_0
        self.no_empty_if_below = no_empty_if_below

    def get_distances(self):
        dist_matrix = np.zeros((self.n_sensors+1,self.n_sensors+1))
        for (node_from, node_to) in combinations(range(self.n_sensors), 2):
            sensor_from = self.sensor_data.iloc[node_from]
            sensor_to = self.sensor_data.iloc[node_to]
            origins = [
                sensor_from["geo_point_2d"].split(", ")
            ]
            destinations = [
                sensor_to["geo_point_2d"].split(", ")
            ]

            matrix = self.gmaps.distance_matrix(
                origins, 
                destinations, 
                mode="driving", 
                language="de-CH",
                departure_time=self.day, # TODO: use specific date/time (also relevant for optimization)
                traffic_model="pessimistic"
            )
            distance_in_seconds = matrix["rows"][0]["elements"][0]["duration"]["value"]

            dist_matrix[node_from][node_to] = distance_in_seconds
            dist_matrix[node_to][node_from] = distance_in_seconds

        # Get distances to sensor_0 which
        for node_to in range(self.n_sensors):
            sensor_to = self.sensor_data.iloc[node_to]
            origins = [
                self.station_0
            ]
            destinations = [
                sensor_to["geo_point_2d"].split(", ")
            ]

            matrix = self.gmaps.distance_matrix(
                origins, 
                destinations, 
                mode="driving", 
                language="de-CH",
                departure_time=self.day.replace(hour=17), # We go home at 17:00 :)
                traffic_model="pessimistic"
            )
            distance_in_seconds = matrix["rows"][0]["elements"][0]["duration"]["value"]

            # Set weights of edges to inverse of level given by the sensor
            dist_matrix[-1][node_to] = distance_in_seconds
            dist_matrix[node_to][-1] = distance_in_seconds

        return dist_matrix
    
    def get_costs(self, dist_matrix):
        cost_matrix = np.zeros((self.n_sensors+1,self.n_sensors+1))
        for (node_from, node_to) in combinations(range(self.n_sensors), 2):
            sensor_from = self.sensor_data.iloc[node_from]
            sensor_to = self.sensor_data.iloc[node_to]

            # Set weights of edges to inverse of level given by the sensor
            cost_matrix[node_from][node_to] = (dist_matrix[node_from][node_to] / sensor_to["level"]) if sensor_to["level"] > self.no_empty_if_below else np.inf
            cost_matrix[node_to][node_from] = (dist_matrix[node_to][node_from] / sensor_from["level"]) if sensor_from["level"] > self.no_empty_if_below else np.inf
       
        for node_to in range(self.n_sensors):
            sensor_to = self.sensor_data.iloc[node_to]
            cost_matrix[-1][node_to] = dist_matrix[-1][node_to] / sensor_to["level"]
            cost_matrix[node_to][-1] = dist_matrix[node_to][-1]

        return cost_matrix

    def generate_map(self, visited_stops: list, show_min_max_markers: bool = False):
        points = []
        markers = []
        for stop in visited_stops:
            if stop != -1:
                sensor = self.sensor_data.iloc[stop]
                location = sensor["geo_point_2d"].split(", ")
                markers.append(StaticMapMarker(
                    locations=[location],
                    size="tiny",
                    color="red",
                    #label=chr(ord('a') + -32 + stop),
                ))
            else:
                location = self.station_0
            points.append(location)
        markers.append(StaticMapMarker(
            locations=[self.station_0],
            size="tiny",
            color="blue",
        ))

        def add_min_max_markers():
            all_coordinates = np.array([np.array(x.split(", "), dtype=np.float32) for x in self.sensor_data['geo_point_2d']])
            min_lng = np.argmin(all_coordinates[:,0])
            max_lng = np.argmax(all_coordinates[:,0])
            min_lat = np.argmin(all_coordinates[:,1])
            max_lat = np.argmax(all_coordinates[:,1])
            coord_min_lng = all_coordinates[min_lng]
            coord_max_lng = all_coordinates[max_lng]
            coord_min_lat = all_coordinates[min_lat]
            coord_max_lat = all_coordinates[max_lat]
            markers.append(StaticMapMarker(
                locations=[coord_min_lng, coord_max_lng, coord_min_lat, coord_max_lat],
                size="tiny",
                color="green",
            ))
        if show_min_max_markers:
            add_min_max_markers()

        st_gallen = (47.4245, 9.3767)
        path = StaticMapPath(
            points=points,
            weight=1,
            color="blue",
        )
        return self.gmaps.static_map(
            size=(700, 350),
            zoom=12,
            center=st_gallen,
            maptype="satellite",
            format="png",
            scale=4,
            path=path,
            markers=markers
        )
