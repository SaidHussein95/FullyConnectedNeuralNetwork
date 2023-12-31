import numpy as np
from Base import BaseLayer


class FullyConnected(BaseLayer):
    def __init__(self, input_size, output_size):
        BaseLayer.__init__(self)  # Super_constructor
        self.input_size = input_size
        self.output_size = output_size
        self.trainable = True
        self.weights = np.random.uniform(0, 1, (self.input_size+1, self.output_size))
        self._gradient_weights = None
        self._optimizer = None
        self._last_input = None

    def forward(self, input_tensor):

        # input_tensor: Input tensor with dim [b=batch_size, n=input_size]
        # output: Output tensor with dim [b, m=output_size]

        one_vec = np.ones((input_tensor.shape[0], 1))  # dim: [b,1] for bias
        self._last_input = np.concatenate((input_tensor, one_vec), axis=1)
        output = np.dot(self._last_input, self.weights)
        return output

    def backward(self, error_tensor):

        # error_tensor: dl/dx with dim [b, m = output_size]
        # output: error tensor for previous layer with dim [b, n = input_size]

        self._gradient_weights = np.dot(self._last_input.T, error_tensor)  # dim=[n+1, m]
        error_tensor = np.dot(error_tensor, self.weights.T[:, :-1])  # dim = [b, n] error tensor for the previous layer
        if self._optimizer:  # update weights
            self.weights = self._optimizer.calculate_update(self.weights, self._gradient_weights)
        return error_tensor

    @property        # set and return the members of optimizer
    def optimizer(self):
        return self._optimizer

    @optimizer.setter
    def optimizer(self, val):
        self._optimizer = val

    @property
    def gradient_weights(self):
        return self._gradient_weights

    @gradient_weights.setter
    def gradient_weights(self, val):
        self._gradient_weights = val
