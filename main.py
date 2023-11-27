from numpy import array

from lib.models.vanilla_lstm import VanillaLSTM
from lib.preprocessing import read_data, sequence_data, get_sensor_values, get_training_data

data = read_data('data/fill-level.csv')
test_sensor = get_sensor_values(data, '107075 | 2B2A')
training_data = get_training_data(data)

train_x, train_y = sequence_data(training_data, 5)
#for index, x in enumerate(train_x):
#    print(x, '->', train_y[index])


vanilla_lstm_model = VanillaLSTM(step_size=5)
vanilla_lstm_model.train(train_x, train_y, 40)
example_data = array([0.18987179, 0.21141369, 0.2417378, 0.29216755, 0.295375, 0.3538226744186046])
prediction = vanilla_lstm_model.predict(example_data[:5])
print(f'prediction: {prediction[0]}, truth: {example_data[5]}')  # prediction: 0.31279, truth: 0.35382
