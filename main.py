from numpy import array
import pandas as pd

from lib.models.vanilla_lstm import VanillaLSTM
from lib.preprocessing import read_data, sequence_data, get_sensor_values, get_training_data, split_data


STEP_SIZE = 5

columns = [
    'sensor_id','date','geo_point_2d','level','type'
]
raw_data = pd.read_csv("data/days_merged.csv", delimiter=',', usecols=columns)
raw_data.sort_values(["sensor_id", "date"], inplace=True)
# test_sensor = get_sensor_values(data, '107075 | 2B2A')
raw_train, raw_test = split_data(data=raw_data, ratio=0.9)
train = get_training_data(raw_train)
test = get_training_data(raw_test)

train_x, train_y = sequence_data(train, STEP_SIZE)
test_x, test_y = sequence_data(test, STEP_SIZE)
#for index, x in enumerate(train_x):
#    print(x, '->', train_y[index])

# EXAMPLE: Create model

vanilla_lstm_model = VanillaLSTM(step_size=STEP_SIZE)
vanilla_lstm_model.train(train_x, train_y, 3, 'trained_models/vanilla-lstm')
accuracy = vanilla_lstm_model.test(test_x, test_y)
print('accuracy:', round(100 * accuracy, 3), '%')


# EXAMPLE: Load model from disk
model = VanillaLSTM(step_size=STEP_SIZE, load_from='trained_models/vanilla-lstm-1')
#accuracy = model.test(test_x, test_y)
#print(accuracy)
model.summary()
val = model.predict(array([0.1, 0.2, 0.3, 0.4, 0.5]))
print(val)
