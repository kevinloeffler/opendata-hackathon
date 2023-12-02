from numpy import array

from lib.models.vanilla_lstm import VanillaLSTM
from lib.preprocessing import read_data, sequence_data, get_sensor_values, get_training_data, split_data


STEP_SIZE = 5


raw_data = read_data('data/fill-level.csv')
# test_sensor = get_sensor_values(data, '107075 | 2B2A')
raw_train, raw_test = split_data(data=raw_data, ratio=0.9)
train = get_training_data(raw_train)[0: 100]
test = get_training_data(raw_test)[0: 100]

train_x, train_y = sequence_data(train, STEP_SIZE)
test_x, test_y = sequence_data(test, STEP_SIZE)
#for index, x in enumerate(train_x):
#    print(x, '->', train_y[index])

# EXAMPLE: Create model
'''
vanilla_lstm_model = VanillaLSTM(step_size=STEP_SIZE)
vanilla_lstm_model.train(train_x, train_y, 40, 'trained_models/vanilla-lstm')
accuracy = vanilla_lstm_model.test(test_x, test_y)
print('accuracy:', round(100 * accuracy, 3), '%')
'''

# EXAMPLE: Load model from disk
model = VanillaLSTM(step_size=STEP_SIZE, load_from='trained_models/vanilla-lstm-1')
accuracy = model.test(test_x, test_y)
print(accuracy)
