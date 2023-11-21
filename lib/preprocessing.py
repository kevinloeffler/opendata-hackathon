import pandas as pd

MAX_SENSOR_INPUT = 1600

def read_data(from_path: str, use_coordinates: bool = False, ):
    columns = [
        'Gemessen am',
        'Tags',
        'Füllstandsdistanz',
        'Sensorname',
    ]

    if use_coordinates:
        columns.append('geo_point_2d')

    df = pd.read_csv(from_path, delimiter=';', usecols=columns)
    df = df.rename(columns={'Gemessen am': 'date', 'Tags': 'type', 'Füllstandsdistanz': 'level', 'Sensorname': 'sensor_id'})

    # ids = set(df['sensor_id'])

    # for idx in range(1, len(df)):
        # max_value_per_sensor[df.loc[idx, 'sensor_id']] = max(max_value_per_sensor[df.loc[idx, 'sensor_id']], df.loc[idx, 'level'])

    df['level'] = df['level'].apply(lambda level: normalize_data(level))

    return df


def normalize_data(level: float):
    level = min(level, MAX_SENSOR_INPUT)
    return 1 - (level / MAX_SENSOR_INPUT)
