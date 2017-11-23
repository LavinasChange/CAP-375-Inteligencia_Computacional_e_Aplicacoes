import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

import activation_functions as libfunc
import derivative_fucntions as deriFunc


class MLP:
    def __init__(self, epochs, train_data, valid_data, test_data, learning_rate=0.5, momentum=1, rmse_min=1000,
                 stop_params="epochs"):
        self._epochs = epochs
        self._train_data = train_data
        self._valid = valid_data
        self._test_data = test_data
        self._learning_rate = learning_rate
        self._momentum = momentum
        self._stop_params = stop_params
        self._rmse_min = rmse_min
        self._weights0 = 2 * np.random.random((15, 8)) + 1
        self._weights1 = 2 * np.random.random((8, 1)) + 1

    def train(self):
        rmseArray = []
        epoch = self._epochs
        # condicao de parada por epocas
        while epoch > 0:

            np.random.shuffle(self._train_data)

            train_X = self._train_data[:, :15]
            Y = self._train_data[:, -1]
            train_Y = []
            for y in Y:
                train_Y.append([y])

            train_Y = np.asarray(train_Y)
            print("Epoch: " + str(epoch))

            inputLayer = train_X

            # Camada de entrada
            sum_sinapse0 = np.dot(inputLayer, self._weights0)
            hiddenLayer = libfunc.sigmoid(sum_sinapse0)

            sum_sinapse1 = np.dot(hiddenLayer, self._weights1)
            outputLayer = libfunc.sigmoid(sum_sinapse1)

            outputLayerError = train_Y - outputLayer

            # Condição
            rmse = mean_squared_error(train_Y, outputLayer)
            rmseArray.append(np.mean(outputLayerError))
            if rmse < self._rmse_min and self._stop_params == "mse":
                break

            derivedOutput = deriFunc.derived_sigmoid(outputLayer)
            deltaOutput = outputLayerError * derivedOutput

            weight1T = self._weights1.T
            deltaOutXWeight = deltaOutput.dot(weight1T)
            deltaOutputHidden = deltaOutXWeight * deriFunc.derived_sigmoid(hiddenLayer)

            hiddenLayerT = hiddenLayer.T
            weight1_new = hiddenLayerT.dot(deltaOutput)
            self._weights1 = (self._weights1 * self._momentum) + (weight1_new * self._learning_rate)

            inputLayerT = inputLayer.T
            weight0_new = inputLayerT.dot(deltaOutputHidden)
            self._weights0 = (self._weights0 * self._momentum) + (weight0_new * self._learning_rate)

            # implementar validacao cruzada
            cross_stop = False

            if cross_stop and self._stop_params == "crossvalidation":
                break

            epoch -= 1
            # fim de todas epocas
            np.savetxt("RMSE.txt", rmseArray, fmt='%1.6f')
        plt.clf()
        plt.plot(rmseArray)
        plt.grid()
        plt.show()
        #plt.savefig(os.path.dirname(__file__) + "\\graphs\\train\\" + "train_" + str(self._epochs) + ".png")

    def test(self):
        test_X = self._test_data[:, :15]
        Y = self._test_data[:, -1]

        inputLayer = test_X

        sum_sinapse0 = np.dot(inputLayer, self._weights0)
        hiddenLayer = libfunc.sigmoid(sum_sinapse0)

        sum_sinapse1 = np.dot(hiddenLayer, self._weights1)
        outputLayer = libfunc.sigmoid(sum_sinapse1)
        print()
        plt.clf()
        plt.plot(Y)
        plt.plot(outputLayer)
        plt.legend(['Observed', 'Predict'], loc='upper right')
        plt.grid()
        plt.savefig(os.path.dirname(__file__) + "\\graphs\\test\\" + "test_" + str(self._epochs) + ".png")
