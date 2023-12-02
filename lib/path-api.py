'''
Run from root directory:
flask --app lib/path-api run
'''
from flask import Flask
from preprocessing import read_data
from map_service import MapService
from path_finder import PathFinder

app = Flask(__name__)
data_file = 'data/fill-level.csv'

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.replace('\n', '').split('='))
        for line in fh.readlines() if not line.startswith('#')
    )

n_sensors = 42 # Number of sensors in St. Gallen
no_empty_if_below = 0.4
station_0 = (47.4156038, 9.3325804) # Assumption: Empyting starts and ends at Kehrichtheizkraftwerk St.Gallen
sensor_data = read_data(data_file, use_coordinates=True)
sensor_data = sensor_data.loc[sensor_data.groupby('sensor_id').date.idxmax()] # Get sensor_id only once

map_service = MapService(vars_dict["MAPS_KEY"], sensor_data, n_sensors, station_0, no_empty_if_below)
path_finder = PathFinder(map_service, sensor_data, station_0, n_sensors)

@app.route("/path", methods=['GET'])
def get_path():
    visited_stops, needed_time = path_finder.find_path()
    print(needed_time)
    return "Hello, World!"