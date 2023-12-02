# path_api.py
import datetime
from flask import Blueprint, jsonify, request
from models.vanilla_lstm import VanillaLSTM
from preprocessing import read_data
from map_service import MapService
from path_finder import PathFinder
import numpy as np
import pandas as pd

data_file = 'data/days_merged.csv'

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.replace('\n', '').split('='))
        for line in fh.readlines() if not line.startswith('#')
    )

n_sensors = 42 # Number of sensors in St. Gallen
station_0 = (47.4156038, 9.3325804) # Assumption: Empyting starts and ends at Kehrichtheizkraftwerk St.Gallen

columns = [
    'sensor_id','date','geo_point_2d','level','type'
]
sensor_data_raw = pd.read_csv(data_file, delimiter=',', usecols=columns)

path_api = Blueprint('path_api', __name__)


STEP_SIZE = 5
model = VanillaLSTM(step_size=STEP_SIZE, load_from='trained_models/vanilla-lstm-1')


no_empty_if_below = 0.4
n_days = 5

def get_next_n_days(n_days: int, no_empty_if_below: float):
    all_needed_time = []
    all_needed_capacity = []
    all_visited_locations = []
    all_predictions = {}
    sensor_data_copy = sensor_data_raw.copy() # holds the predicted values after first iteration

    for i in range(n_days):
        sensor_data = sensor_data_copy.loc[sensor_data_copy.groupby('sensor_id').date.idxmax()] # Get sensor_id only once

        if i > 0 and np.count_nonzero([v[-1] for k,v in all_predictions.items()]) == 0:
            # all containers have been emptied previously
            print("All containers have been emptied...")
            break

        #all_predictions holds the predictions for each sensor per iteration of n_days

        map_service = MapService(vars_dict["MAPS_KEY"], sensor_data, n_sensors, station_0, no_empty_if_below)
        path_finder = PathFinder(map_service, sensor_data, station_0, n_sensors)

        _, needed_time, visited_stations, needed_capacity = path_finder.find_path()
        visited_stations_by_id = [x["sensor_id"] for x in visited_stations[1:-1]]
        print(needed_capacity)
        print(visited_stations_by_id)

        all_needed_time.append(needed_time)
        all_needed_capacity.append(needed_capacity)
        all_visited_locations.append(visited_stations)

        # calculate predictions for next iteration
        for sensor_id, values_raw in list(sensor_data_raw.groupby('sensor_id')):
            last_5_values = values_raw.sort_values(by="date").tail(5-i)["level"].to_numpy()
            if all_predictions.get(sensor_id):
                # merge previous predictions with last n values
                last_5_values = np.append(last_5_values, all_predictions[sensor_id])
            else:
                all_predictions[sensor_id] = []
            for j in range(1, len(last_5_values)):
                if (last_5_values[j] - last_5_values[j-1]) < -0.02:
                    # Data has been emtpied - set data before jump to 0
                    last_5_values[:j] = 0
            all_predictions[sensor_id].append(model.predict(last_5_values).ravel()[0])

        # add predictions to dataset for next iteration
        pred_date = datetime.date.today() + datetime.timedelta(days=i)
        for sensor_id, predictions in all_predictions.items():
            #has_been_emptied = np.in1d(sensor_id, visited_stations_by_id)[0]
            #if has_been_emptied:
            #    predictions[-1] = 0 # updates value in all_predictions

            sensor = sensor_data[sensor_data["sensor_id"] == sensor_id].iloc[0]
            new_entry = pd.Series({
                'sensor_id': sensor_id, 
                'date': pred_date.strftime('%Y-%m-%d'), 
                'geo_point_2d': sensor["geo_point_2d"],
                'level': predictions[-1], # has been emptied
                'type': sensor["type"]
            })
            sensor_data_copy.loc[len(sensor_data_copy)] = new_entry

    return all_needed_time, all_needed_capacity, all_visited_locations

#get_next_n_days(n_days, no_empty_if_below)

@path_api.route("", methods=['GET'])
def get_path():
    selected_date = request.args.get('date')
    no_empty_if_below = float(request.args.get('no_empty_if_below')) if request.args.get('no_empty_if_below') is not None else 0.4
    glass_type_list = request.args.get('glass_type_list').split(",") if request.args.get('glass_type_list') is not None else None

    all_needed_time, all_needed_capacity, all_visited_locations = get_next_n_days(5, no_empty_if_below)

    return jsonify({"visited_locations": all_visited_locations, "needed_times": all_needed_time, "needed_capacities": all_needed_capacity})