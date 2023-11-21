from lib.preprocessing import read_data, reformat, split_data, normalize_data
from lib.model import train_model

data = read_data('/home/ubuntu16/Documents/OST/5Sem2023HS/ml/hackaton/fullstandssensoren-sammelstellen-stadt-stgallen.csv')
#print(data.iloc[2: 10])
#data = normalize_data(data)

train_data, test_data = split_data(data, 0.8)

train_x, train_y = reformat(train_data[10:20], 5)
#print('output', train_x)
#print(len(data), len(train_data), len(test_data))

train_model(train_x, train_y)
