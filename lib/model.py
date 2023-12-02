import os
from abc import ABC, abstractmethod

import numpy as np
from numpy import array
from tensorflow import keras
import matplotlib.pyplot as plt


class BaseModel(ABC):

    @abstractmethod
    def __init__(self, step_size: int):
        raise NotImplemented

    @abstractmethod
    def train(self, train_x: array, train_y: array, epochs: int, safe_to: str):
        raise NotImplemented

    @abstractmethod
    def predict(self, data: array):
        raise NotImplemented

    def test(self, test_x: array, test_y: array) -> float:
        # Currently only returns one accuracy, could be extended with more metrics, eg. std-err...
        predictions = []
        accuracies = []
        for i in range(len(test_y)):
            prediction = (self.predict(test_x[i]))
            print(f'prediction: {prediction}, truth: {test_y[i]}')
            predictions.append(prediction)
            accuracies.append(abs(prediction - test_y[i]))
        self.__plot_test(predictions=predictions, truths=test_y)
        return 1 - np.average(accuracies)

    @staticmethod
    def __plot_test(predictions: array, truths: array):
        x_values = np.arange(len(predictions))
        plt.plot(x_values, predictions, label='Predictions')
        plt.plot(x_values, truths, label='Truths')
        plt.legend()
        plt.show()

    def save_model(self, path: str):
        json = self.model.to_json()
        output_dir = self.get_output_dir(path)
        os.mkdir(output_dir)
        with open(f'{output_dir}/model.json', 'x') as file:
            file.write(json)
        self.model.save_weights(f'{output_dir}/model.h5')
        print('saved model')

    @staticmethod
    def get_output_dir(path) -> str:
        p = path
        index = 1
        while os.path.exists(f'{p}-{index}'):
            index += 1
        return f'{p}-{index}'

    def load(self, path: str):
        with open(f'{path}/model.json', 'r') as file:
            json_model = file.read()
        model = keras.models.model_from_json(json_model)
        model.load_weights(f'{path}/model.h5')
        self.model = model
        print('model loaded from disk')
