# -*- coding: utf-8 -*-
"""ME18B181_ME18B182_q2_bonus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zP0xX89LrbIgV6yx7uaWqv6PEWSGZ60k
"""

import numpy as np
from tqdm.auto import tqdm
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

class ANN:
    def __init__(self, intermediate_size, activation_fn=np.tanh):
        self._parameters = self._init_params([1, intermediate_size, 1])
        self._activation_fn = activation_fn

    def parameters(self):
        return self._parameters

    def update_params(self, params):
        self._parameters = params

    @staticmethod
    def _init_params(sizes):
        params = {}
        for i in range(1, len(sizes)):
            params[f"w{i}"] = np.random.normal(scale=0.01, size=(sizes[i], sizes[i - 1]))
            params[f"b{i}"] = np.random.normal(scale=0.01, size=(sizes[i], 1))
        return params

    def forward(self, inputs):
        num_layers = len(self._parameters) // 2
        activations = {}
        for i in range(1, num_layers+1):
            if i == 1:
                activations[f"z{i}"] = self._parameters[f"w{i}"] @ inputs + self._parameters[f"b{i}"]
                activations[f"a{i}"] = self._activation_fn(activations[f"z{i}"])
            else:
                activations[f"z{i}"] = self._parameters[f"w{i}"] @  activations[f"a{i-1}"] + self._parameters[f"b{i}"]
                if i == num_layers:
                    activations[f"a{i}"] = activations[f"z{i}"]
                else:
                    activations[f"a{i}"] = self._activation_fn(activations[f"z{i}"])
        return activations

    def backward(self, activations, inputs, targets):
        num_layers = len(self._parameters)//2
        m = len(targets)
        grads = {}
        for i in range(num_layers, 0, -1):
            if i == num_layers:
                dA = 1/m * (activations[f"a{i}"] - targets)
                dZ = dA
            else:
                dA = (self._parameters[f"w{i+1}"].T @ dZ) * (1 - np.tanh(self._parameters[f"w{i+1}"] @ activations[f"a{i}"] + self._parameters[f"b{i}"]) ** 2)
                dZ = np.multiply(dA, np.where(activations[f"a{i}"] >= 0, 1, 0))
            if i==1:
                grads[f"w{i}"] = 1/m * (dZ @ inputs.T)
                grads[f"b{i}"] = 1/m * np.sum(dZ, axis=1, keepdims=True)
            else:
                grads[f"w{i}"] = 1/m * (dZ @ activations[f"a{i-1}"].T)
                grads[f"b{i}"] = 1/m * np.sum(dZ, axis=1, keepdims=True)
        return grads


def optimizer_step(params, grads, lr):
    num_layers = len(params) // 2
    new_params = {}
    for i in range(1, num_layers+1):
        new_params[f"w{i}"] = params[f"w{i}"] - lr * grads[f"w{i}"]
        new_params[f"b{i}"] = params[f"b{i}"] - lr * grads[f"b{i}"]
    return new_params


def train(X, y, intermediate_size, n_epochs, lr):
    model = ANN(intermediate_size)

    for _ in range(1, n_epochs + 1):
        activations = model.forward(X)
        grads = model.backward(activations, X, y.T)
        new_params = optimizer_step(model.parameters(), grads, lr)
        model.update_params(new_params)

    return model


def compute_score(model, X, y):
    activations = model.forward(X)
    score = np.sqrt(mean_squared_error(y, activations["a2"].T))
    return score

ages = [15, 15, 15, 18, 28, 29, 37, 37, 44, 50, 50, 60, 61, 64, 65, 65, 72, 75, 75, 82, 85, 91, 91, 97, 98, 125, 142, 142, 147, 147, 150, 159, 165, 183, 192, 195, 218, 218, 219, 224, 225, 227, 232, 232, 237, 246, 258, 276, 285, 300, 301, 305, 312, 317, 338, 347, 354, 357, 375, 394, 513, 535, 554, 591, 648, 660, 705, 723, 756, 768, 860]
weights = [21.66, 22.75, 22.3, 31.25, 44.79, 40.55, 50.25, 46.88, 52.03, 63.47, 61.13, 81, 73.09, 79.09, 79.51, 65.31, 71.9, 86.1, 94.6, 92.5, 105, 101.7, 102.9, 110, 104.3, 134.9, 130.68, 140.58, 155.3, 152.2, 144.5, 142.15, 139.81, 153.22, 145.72, 161.1, 174.18, 173.03, 173.54, 178.86, 177.68, 173.73, 159.98, 161.29, 187.07, 176.13, 183.4, 186.26, 189.66, 186.09, 186.7, 186.8, 195.1, 216.41, 203.23, 188.38, 189.7, 195.31, 202.63, 224.82, 203.3, 209.7, 233.9, 234.7, 244.3, 231, 242.4, 230.77, 242.57, 232.12, 246.7]
ages, weights = np.array(ages)[None], np.array(weights)

n_epochs = 450
lr = 1e-3
metrics, intermediate_sizes = [], []
for intermediate_size in tqdm(range(10, 1000, 10)):
    trained_model = train(ages, weights, intermediate_size, n_epochs, lr)
    score = compute_score(trained_model, ages, weights)
    metrics.append(score)
    intermediate_sizes.append(intermediate_size)

print("Training Loss for various intermediate sizes", metrics)
plt.plot(intermediate_sizes, metrics)
plt.xlabel("Number of neurons in intermediate layer")
plt.ylabel("Training Loss")
plt.show()