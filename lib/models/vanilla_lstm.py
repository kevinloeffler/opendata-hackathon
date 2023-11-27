import keras

# the model expects training data in the shape: [samples, step size, features]


class VanillaLSTM:
    def __init__(self, step_size):
        self.step_size = step_size
        self.model = keras.Sequential()
        self.model.add(keras.layers.LSTM(units=50, activation='relu', input_shape=(self.step_size, 1)))
        self.model.add(keras.layers.Dense(1))
        self.model.compile(optimizer='adam', loss='mse')

    def train(self, train_x, train_y, epochs: int):
        training_data = train_x.reshape((train_x.shape[0], train_x.shape[1], 1))
        self.model.fit(training_data, train_y, epochs=epochs)

    def predict(self, data):
        input_data = data.reshape((1, self.step_size, 1))
        return self.model.predict(input_data)
