# creating input neurons
import math


class InputNeuron:
    def __init__(self, input_data, weight, bias):
        self.inputData = input_data
        self.weight = weight
        self.bias = bias
        self.output = 0

    def activate(self):
        self.output = math.tanh(self.inputData + self.bias)

    def get_output(self):
        return self.output


class OutputNeuron:
    def __init__(self, connection_ws, inputs, bias):
        self.Ws = connection_ws
        self.inputs = inputs
        self.bias = bias
        self.output = 0

    def activate(self):
        for i in range(0, len(self.inputs)):
            self.output += self.inputs[i] * self.Ws[i]

        self.output += self.bias

    def get_output(self):
        return self.output