import numpy as np

class ToolSet():
    def __init__(self):
        pass

    def step(self, x):
        y = x > 0
        return y.astype(np.int)

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def relu(self, x):
        return np.maximum(0, x)

    def softmax(self, x):
        a = np.max(x)
        exp_x = np.exp(x - a)
        sum_exp_x = np.sum(exp_x)
        y = exp_x / sum_exp_x
        return y

    def mean_squared_error(self, y, t):
        return 0.5 * np.sum((y-t)**2)

    def cross_entropy_error(self, y, t):
        delta = 1e-7
        return -np.sum(t * np.log(y + delta))