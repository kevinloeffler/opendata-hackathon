from numpy import array

from lib.models.vanilla_lstm import VanillaLSTM, VanillaLSTMBiggerStepSize
from lib.preprocessing import read_data, sequence_data, sequence_data_and_day, get_sensor_values, get_training_data_and_day, get_training_data, split_data


STEP_SIZE = 5


raw_data = read_data('data/fill-level.csv')
# test_sensor = get_sensor_values(data, '107075 | 2B2A')
raw_train, raw_test = split_data(data=raw_data, ratio=0.9)
train = get_training_data_and_day(raw_train)
#print(train)
test = get_training_data_and_day(raw_test)
print(len(train), len(test))
train_x, train_y = sequence_data_and_day(train, STEP_SIZE)
test_x, test_y = sequence_data(test, STEP_SIZE)
#for index, x in enumerate(train_x):
#    print(x, '->', train_y[index])

# EXAMPLE: Create model

vanilla_lstm_model = VanillaLSTMandDay(step_size=STEP_SIZE)
vanilla_lstm_model.train(train_x, train_y, 40, 'trained_models/VanillaLSTMandDay')
accuracy = vanilla_lstm_model.test(test_x, test_y)
print('accuracy:', round(100 * accuracy, 3), '%')
'''

# EXAMPLE: Load model from disk
model = VanillaLSTM(step_size=STEP_SIZE, load_from='trained_models/vanilla-lstm-2')
accuracy = model.test(test_x, test_y)
print(accuracy)

'''
