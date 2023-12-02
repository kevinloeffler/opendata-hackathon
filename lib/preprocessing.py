import math
import datetime
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
    days_merged = _merge_days(filtered_data, use_coordinates)
    days_merged['level'] = days_merged['level'].apply(lambda level: normalize_data(level))  # normalise data
    return days_merged

def data_split(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_data = data[0:int(len(data)*0.9)]
    validate_data = data [int(len(data)*0.9):]
    #train_data, validate_data = train_test_split(data, test_size=0.1, random_state=42)
    
    return  train_data, validate_data

def _merge_days(dataframe: pd.DataFrame, use_coordinates):
    dataframe['date'] = pd.to_datetime(dataframe['date'], utc=True).dt.date
    columns = ['sensor_id', 'date']
    if use_coordinates: columns.append('geo_point_2d')
    return dataframe.groupby(columns).agg({'level': 'mean', 'type': 'last'}).reset_index()


def get_sensor_values(dataframe: pd.DataFrame, sensor_name: str) -> list[float]:
    return dataframe[dataframe['sensor_id'] == sensor_name]['level'].tolist()





def get_training_data_and_day(dataframe: pd.DataFrame) -> list[tuple[float, float]]:
    # Extract weekday from 'Gemessen am' column
    dataframe['weekday'] = dataframe['date'].apply(lambda x: x.weekday())/7
    #TODO: map the zyclic propertiy to a sin, or something
    # Create a list of tuples containing 'level' and 'weekday' values
    training_data_and_day = dataframe[['level', 'weekday']].to_records(index=False).tolist()
    return training_data_and_day


def get_training_data(dataframe: pd.DataFrame) -> list[float]:
    return dataframe['level'].tolist()


def normalize_data(level: float):
    level = min(level, MAX_SENSOR_INPUT)
    if math.isnan(1 - (level / MAX_SENSOR_INPUT)):
        print(level)
    return 1 - (level / MAX_SENSOR_INPUT)



def sequence_data_and_day(data: list[tuple[float, float]], step_size: int, sensor_noise: float = 0.1) -> tuple[array, array]:
    x, y = [], []
    for i in range(len(data) - step_size):
        sub_array = data[i: i + step_size]
        if not check_if_array_is_ascending(sub_array) or data[i + step_size][0] < data[i + step_size - 1][0]:  # + sensor_noise:
            continue
        x.append((array([item[0] for item in sub_array]), sub_array[-1][1]))
        y.append(data[i + step_size][0])
    return array(x), array(y)

                 

def sequence_data(data: list[float], step_size: int, sensor_noise: float = 0.1) -> tuple[array, array]:
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
