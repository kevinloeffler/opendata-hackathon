import numpy as np
import tensorflow as tf
import keras
from keras import layers


def train_model(x_train, y_train):
    model = keras.Sequential()
    # Add an Embedding layer expecting input vocab of size 1000, and
    # output embedding dimension of size 64.
    model.add(layers.Embedding(input_dim=1000, output_dim=64))

    # Add a LSTM layer with 128 internal units.
    model.add(layers.LSTM(128))

    # Add a Dense layer with 10 units.
    model.add(layers.Dense(10))

    optimizer = tf.keras.optimizers.Adam(
        learning_rate = 0.001
        )

    model.compile(optimizer=optimizer, loss='mean_squared_error')
    losses = model.fit(x_train, y_train, epochs=3, batch_size = 80)

    print(losses)
    print( model.summary())
    
