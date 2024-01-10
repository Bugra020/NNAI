import math
import random
import numpy


class NeuralModal:
    def __init__(self):
        self.input_w = []
        self.hidden_w = []
        self._setWeights()

        self.input_b = []
        self.hidden_b = []
        self.output_b = []
        self._setBiases()

    def _setWeights(self):
        # for input layer
        for i in range(0, 44):
            w_to_hiddens = []
            for j in range(0, 44):
                ran = random.uniform(-1, 1)
                w_to_hiddens.append(ran)
            self.input_w.append(w_to_hiddens)

        # for hidden layer
        for i in range(0, 44):
            w_to_output = []
            for j in range(0, 1):
                ran = random.uniform(-1, 1)
                w_to_output.append(ran)
            self.hidden_w.append(w_to_output)

    def _setBiases(self):
        # for input layer
        for i in range(0, 44):
            self.input_b.append(0)

        # for hidden layer
        for i in range(0, 44):
            self.hidden_b.append(0)

        # for output neuron
        for i in range(0, 1):
            self.output_b.append(0)

    def _tanh(self, x):
        return numpy.tanh(x)

    def _d_tanh(self, x):
        return numpy.power((1 / numpy.cosh(x)), 2)

    def _cost(self, x):
        return math.pow(x, 2)

    def _d_cost(self, x):
        return 2 * x

    def _input_layer_activation(self, input_dataset):
        layer_output = []  # has length of 44
        for i in range(0, len(input_dataset)):
            a = self._tanh(input_dataset[i] + self.input_b[i])
            layer_output.append(a)

        return layer_output

    def _layer_activation(self, incoming_dataset, weights):
        #                       len = 44           len(w) = 44, len(w[0]) = 44
        layer_output = []  # len = 66
        z = 0
        for hidden_n in range(0, len(weights[0])):
            for input_n in range(0, len(weights)):
                z += incoming_dataset[input_n] * weights[input_n][hidden_n]
            layer_output.append(self._tanh(z + self.hidden_b[hidden_n]))

        return layer_output

    def _layer_cost(self, outputs, target):
        layer_cost = []
        for i in range(0, len(outputs)):
            c = math.pow((outputs[i] - target), 2)
            layer_cost.append(c)

        return layer_cost

    def _update_weight(self, e, z, cost):
        return e * z * self._d_tanh(z) * self._d_cost(cost)

    def _update_bias(self, e, z, cost):
        return e * 1 * self._d_tanh(z) * self._d_cost(cost)

    def _update_input_layer(self, input_data, costs, e):
        z = 0
        for i in range(0, 44):
            z = input_data[i]

            for j in range(0, 44):
                self.input_w[i][j] -= self._update_weight(e, z, costs[i])

            self.input_b[i] -= self._update_bias(e, z, costs[i])

    def _update(self, pre_output, costs, e):
        for hidden in range(0, 44):
            z = 0
            for a in range(0, 44):
                z += pre_output[a] * self.input_w[a][hidden]

            self.hidden_w[hidden][0] -= self._update_weight(e, z, costs[hidden])
            self.hidden_b[hidden] -= self._update_bias(e, z, costs[hidden])

    def _update_final(self, pre_output, cost, e):
        z = 0
        for a in range(0, 44):
            z += pre_output[a] * self.hidden_w[a][0]
        self.output_b[0] -= self._update_bias(e, z, cost)

    def train(self, traindata, targets, learning_rate, iterations):
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
        cumulative_errors = []
        for i in range(0, iterations):
            rindex = random.randint(0, len(traindata)-1)
            # input layer
            layerI_o = self._input_layer_activation(traindata[rindex])
            layerI_cost = self._layer_cost(layerI_o, targets[rindex])
            self._update_input_layer(traindata[rindex], layerI_cost, learning_rate)

            # hidden layer
            hidden_layer_o = self._layer_activation(layerI_o, self.input_w)
            hidden_layer_cost = self._layer_cost(hidden_layer_o, targets[rindex])
            self._update(layerI_o, hidden_layer_cost, learning_rate)

            # output neuron/layer
            final_output = self._layer_activation(hidden_layer_o, self.hidden_w)
            final_cost = self._layer_cost(final_output, targets[rindex])
            self._update_final(hidden_layer_o, final_cost[0], learning_rate)

            print(f"{final_output[0]}, {targets[rindex]}, {numpy.sqrt(final_cost[0])}, {i}")
            cumulative_errors.append(final_output[0] - targets[rindex])
        sumn = 0
        for a in cumulative_errors:
            sumn += a
        avg = sumn / len(cumulative_errors)
        print(f"\nAVARAGE LOSS: {avg}")

    def work(self):
        pass

    def save(self):
        pass
