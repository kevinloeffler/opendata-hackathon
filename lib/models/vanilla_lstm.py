import keras
import numpy as np
from lib.model import BaseModel

# the model expects training data in the shape: [samples, step size, features]


class VanillaLSTM(BaseModel):
    def __init__(self, step_size, load_from: str = None):
        self.step_size = step_size

        if load_from:
            self.load(load_from)
        else:
            self.model = keras.Sequential()
            self.model.add(keras.layers.LSTM(units=50, activation='relu', input_shape=(self.step_size, 1)))
            self.model.add(keras.layers.Dense(1))
            self.model.compile(optimizer='adam', loss='mse')

    def train(self, train_x, train_y, epochs: int, safe_to: str):
        print(f'Start training with {len(train_x)} datapoints...')
        training_data = train_x.reshape((train_x.shape[0], train_x.shape[1], 1))
        self.model.fit(training_data, train_y, epochs=epochs)
        self.save_model(safe_to)

    def predict(self, data):
        input_data = data.reshape((1, self.step_size, 1))
        return self.model.predict(input_data)[0]



class VanillaLSTMBiggerStepSize(BaseModel):
    def __init__(self, step_size, load_from: str = None):
        self.step_size = step_size*2

        if load_from:
            self.load(load_from)
        else:
            self.model = keras.Sequential()
            self.model.add(keras.layers.LSTM(units=50, activation='relu', input_shape=(self.step_size, 1)))
            self.model.add(keras.layers.Dense(1))
            self.model.compile(optimizer='adam', loss='mse')

    def train(self, train_x, train_y, epochs: int, safe_to: str):
        print(f'Start training with {len(train_x)} datapoints...')
        training_data = train_x.reshape((train_x.shape[0], train_x.shape[1], 1))
        self.model.fit(training_data, train_y, epochs=epochs)
        self.save_model(safe_to)

    def predict(self, data):
        input_data = data.reshape((1, self.step_size, 1))
        return self.model.predict(input_data)[0]
    
class VanillaLSTMandDay(BaseModel):
    def __init__(self, step_size, load_from: str = None):
        self.step_size = step_size

        if load_from:
            self.load(load_from)
        else:
            self.model = keras.Sequential()
            self.model.add(keras.layers.LSTM(units=50, activation='relu', input_shape=(self.step_size, 2)))
            self.model.add(keras.layers.Dense(1))
            self.model.compile(optimizer='adam', loss='mse')

    def train(self, train_x, train_y, epochs: int, safe_to: str):
        print(f'Start training with {len(train_x)} datapoints...')
        train_x = np.swapaxes(train_x, 1, 2)
        self.model.fit(train_x, train_y, epochs=epochs)
        self.save_model(safe_to)

    def predict(self, input_data):
        input_data = input_data.reshape((1, self.step_size, 2))
        return self.model.predict(input_data).ravel()[0]
