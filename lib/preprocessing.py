import math

from numpy import array
import pandas as pd


MAX_SENSOR_INPUT = 1600


def read_data(from_path_w: str, from_path_g: str, from_path_b: str, use_coordinates: bool = True):
    columns = [
        'measured_at',
        'data_distance',
        'name',
    ]

    if use_coordinates:
        columns.append('geo_point_2d')
        # TODO: needs to be implemented in later functions (e.g. _merge_days) if really needed
       
        
    raw_data_w = pd.read_csv(from_path_w, delimiter=';', usecols=columns)
    raw_data_w = raw_data_w.rename(columns={'measured_at': 'date', 'data_distance': 'level', 'name': 'sensor_id'})

    #adding type column based on name of csv input file
    glasstype="Weissglas"
    raw_data_w ['type'] = glasstype
    filtered_data_w = raw_data_w[raw_data_w['level'].notna()]  # filter all rows with invalid sensor data
    days_merged_w = _merge_days(filtered_data_w, use_coordinates)
    days_merged_w['level'] = days_merged_w['level'].apply(lambda level: normalize_data(level))  # normalise data
    
    raw_data_g = pd.read_csv(from_path_g, delimiter=';', usecols=columns)
    raw_data_g = raw_data_g.rename(columns={'measured_at': 'date', 'data_distance': 'level', 'name': 'sensor_id'})
    
    #adding type column based on name of csv input file
    glasstype="Grünglas"
    raw_data_g ['type'] = glasstype
    filtered_data_g = raw_data_g[raw_data_g['level'].notna()]  # filter all rows with invalid sensor data
    days_merged_g = _merge_days(filtered_data_g, use_coordinates)
    days_merged_g['level'] = days_merged_g['level'].apply(lambda level: normalize_data(level))  # normalise data
    
    raw_data_b = pd.read_csv(from_path_w, delimiter=';', usecols=columns)
    raw_data_b = raw_data_b.rename(columns={'measured_at': 'date', 'data_distance': 'level', 'name': 'sensor_id'})
    
    #adding type column based on name of csv input file
    glasstype="Braunglas"
    raw_data_b ['type'] = glasstype
    filtered_data_b = raw_data_b[raw_data_b['level'].notna()]  # filter all rows with invalid sensor data
    days_merged_b = _merge_days(filtered_data_b, use_coordinates)
    days_merged_b['level'] = days_merged_b['level'].apply(lambda level: normalize_data(level))  # normalise data

    
    days_merged=pd.concat([days_merged_b,days_merged_g, days_merged_w]).sort_values(by="date")
    
    
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


def get_training_data(dataframe: pd.DataFrame) -> list[float]:
    return dataframe['level'].tolist()


def normalize_data(level: float):
    level = min(level, MAX_SENSOR_INPUT)
    if math.isnan(1 - (level / MAX_SENSOR_INPUT)):
        print(level)
    return 1 - (level / MAX_SENSOR_INPUT)


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


if __name__ == '__main__':
    file_path = "data/days_merged.csv"
    days_merged = read_data("data/data_w.csv", "data/data_g.csv", "data/data_b.csv")
    days_merged.to_csv(file_path,sep=',', index=False) 