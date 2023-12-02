# sensor_api.py
from flask import Blueprint, jsonify
from preprocessing import read_data

sensor_api = Blueprint('sensor_api', __name__)

data_file = 'data/fill-level.csv'

sensor_data = read_data(data_file, use_coordinates=True)
sensor_data = sensor_data.loc[sensor_data.groupby('sensor_id').date.idxmax()]  # Get sensor_id only once


@sensor_api.route("", methods=['GET'])
def get_sensor_data():
    # pandas dataframe to dict
    return jsonify(sensor_data.to_dict('records'))


@sensor_api.route("/<sensor_id>", methods=['GET'])
def get_sensor_data_by_id(sensor_id):
    sensor = sensors_data.get(sensor_id)
    if sensor:
        return jsonify(sensor)
    else:
        return jsonify({'error': 'Sensor not found'}), 404
