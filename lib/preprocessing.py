import math

from numpy import array
import pandas as pd

MAX_SENSOR_INPUT = 1600


def read_data(from_path: str, use_coordinates: bool = False):
    columns = [
        'Gemessen am',
        'Tags',
        'Füllstandsdistanz',
        'Sensorname',
    ]

    if use_coordinates:
        columns.append('geo_point_2d')
        # TODO: needs to be implemented in later functions (e.g. _merge_days) if really needed

    raw_data = pd.read_csv(from_path, delimiter=';', usecols=columns)
    raw_data = raw_data.rename(columns={'Gemessen am': 'date', 'Tags': 'type', 'Füllstandsdistanz': 'level', 'Sensorname': 'sensor_id'})

    filtered_data = raw_data[raw_data['level'].notna()]  # filter all rows with invalid sensor data
    days_merged = _merge_days(filtered_data)
    days_merged['level'] = days_merged['level'].apply(lambda level: normalize_data(level))  # normalise data
    return days_merged


def _merge_days(dataframe: pd.DataFrame):
    dataframe['date'] = pd.to_datetime(dataframe['date'], utc=True).dt.date
    return dataframe.groupby(['sensor_id', 'date']).agg({'level': 'mean', 'type': 'last'}).reset_index()


def get_sensor_values(dataframe: pd.DataFrame, sensor_name: str) -> list[float]:
    return dataframe[dataframe['sensor_id'] == sensor_name]['level'].tolist()


def get_training_data(dataframe: pd.DataFrame) -> list[float]:
    return dataframe['level'].tolist()


def normalize_data(level: float):
    level = min(level, MAX_SENSOR_INPUT)
    if math.isnan(1 - (level / MAX_SENSOR_INPUT)):
        print(level)
    return 1 - (level / MAX_SENSOR_INPUT)


def sequence_data(data: list[float], step_size: int, sensor_noise: float = 0.1):
    x, y = [], []
    for i in range(len(data) - step_size):
        sub_array = data[i: i + step_size]
        if not check_if_array_is_ascending(sub_array) or data[i + step_size] < data[i + step_size - 1]:  # + sensor_noise:
            continue
        x.append(data[i: i + step_size])
        y.append(data[i + step_size])
    return array(x), array(y)


def check_if_array_is_ascending(array: list[float]) -> bool:
    for i in range(len(array) - 1):
        if array[i] > array[i + 1]:
            return False
    return True


def split_data(data: pd.DataFrame, ratio: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    total_len = len(data)
    return data[0:round(total_len * ratio)], data[round(total_len * ratio):]
