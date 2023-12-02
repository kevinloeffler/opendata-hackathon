# path_api.py
from flask import Blueprint, jsonify, request, Response
import json
from preprocessing import read_data
from map_service import MapService
from path_finder import PathFinder

data_file = 'data/fill-level.csv'

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.replace('\n', '').split('='))
        for line in fh.readlines() if not line.startswith('#')
    )

n_sensors = 42 # Number of sensors in St. Gallen
station_0 = (47.4156038, 9.3325804) # Assumption: Empyting starts and ends at Kehrichtheizkraftwerk St.Gallen
sensor_data = read_data(data_file, use_coordinates=True)
sensor_data = sensor_data.loc[sensor_data.groupby('sensor_id').date.idxmax()] # Get sensor_id only once

path_api = Blueprint('path_api', __name__)


@path_api.route("", methods=['GET'])
def get_path():
    selected_date = request.args.get('date')
    no_empty_if_below = float(request.args.get('no_empty_if_below')) if request.args.get('no_empty_if_below') is not None else 0.4
    glass_type_list = request.args.get('glass_type_list').split(",") if request.args.get('glass_type_list') is not None else None

    map_service = MapService(vars_dict["MAPS_KEY"], sensor_data, n_sensors, station_0, no_empty_if_below)
    path_finder = PathFinder(map_service, sensor_data, station_0, n_sensors)

    _, needed_time, visited_locations = path_finder.find_path()
    return jsonify({"visited_locations": visited_locations, "needed_time": needed_time})