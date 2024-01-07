import math
import random


class NeuralModal:
    def __init__(self):
        self.weights = []
        self.setWeights()

        self.biases = []
        self.setBiases()

    def setWeights(self):
        for i in range(0, 45):
            ranW = random.uniform(-1, 1)
            self.weights.append(ranW)

    def setBiases(self):
        layer_bs = []
        bForO = [0]
        for i in range(0, 45):
            layer_bs.append(0)

        self.biases.append(layer_bs)
        self.biases.append(bForO)

    def tanh(self, x):
        return math.tanh(x)

    def d_tanh(self, x):
        return math.pow((1 / math.cosh(x)), 2)

    def cost(self, x):
        return math.pow(x, 2)

    def d_cost(self, x):
        return 2*x

    def input_layer_activation(self, dataset):
        layer_output = []
        for i in range(0, len(dataset)):
            a = self.tanh(dataset[i] + self.biases[i])
            layer_output.append(a)

        return layer_output

    def layer_activation(self, dataset, weights):
        layer_output = []
        a = 0
        for i in range(0, len(dataset)):
            a += self.tanh(dataset[i] * weights[i] + self.biases[1][0])
            layer_output.append(a)

        return layer_output

    def layer_cost(self, outputs, targets):
        layer_cost = []
        for i in range(0, len(outputs)):
            c = math.pow((outputs[i] - targets[i]), 2)
            layer_cost.append(c)

        return layer_cost

    def update_weight(self, e, z, cost):
        return e * z * self.d_tanh(z) * self.d_cost(cost)

    def uptade_bias(self, e, z, cost):
        return e * 1 * self.d_tanh(z) * self.d_cost(cost)

    def uptade(self, dataset, costs, e):
        z = 0
        for data in dataset:
            z += data

        # first updating weights
        for i in range(0, len(self.weights)):
            self.weights[i] -= self.update_weight(e, z, costs[i])

        # updating biases
        for i in range(0, len(self.biases[0])):
            self.biases[0][i] -= self.uptade_bias(e, z, costs[i])

    def train(self, traindata, targets, learning_rate):

        """
        compute for input layer
        compute loss/cost
        update the weights biases for input layer
        compute for output layer
        compute loss/cost
        saved it for keeping track of the learning
        update the weight bias
        do this cycle for every training data
        in the end save the weights and biases to config file
        """
        for i in range(0, len(traindata)):
            # first layer
            layer_o = self.input_layer_activation(traindata[i])
            layer_cost = self.layer_cost(layer_o, targets[i])
            self.uptade(traindata[i], layer_cost, learning_rate)

            # output neuron
            final_output = self.layer_activation(layer_o, self.weights)
            final_cost = self.layer_cost(final_output, targets[i])
            self.uptade(layer_o, final_cost, learning_rate)

            print(final_cost)

    def work(self):
        pass

    def save(self):
        pass
