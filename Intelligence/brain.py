import numpy as np

from Globals import globalFcns

# outputs:
#   0   right
#   1   down
#   2   left
#   3   up

class Brain():
    def __init__(self, noOfNeuron1=18, noOfNeuron2=12):
        self.noOfInputs = 24
        self.noOfNeuron1Layer = noOfNeuron1
        self.noOfNeuron2Layer = noOfNeuron2
        self.noOfOutputs = 4

        self.inputs = np.ones((self.noOfInputs, 1))
        self.neuron1Layer = np.zeros((self.noOfNeuron1Layer, 1))
        self.neuron2Layer = np.zeros((self.noOfNeuron2Layer, 1))
        self.neuronLastLayer = np.zeros((self.noOfOutputs, 1), dtype=np.float64)
        self.outputs = np.zeros((self.noOfOutputs, 1))
        self.outputList = [0] * self.noOfOutputs

        self.randomWeights()

    def randomWeights(self):
        strength = 0.2
        self.weights1 = (2 * np.random.random((self.noOfNeuron1Layer, self.noOfInputs)) - 1) * strength
        self.weights2 = (2 * np.random.random((self.noOfNeuron2Layer, self.noOfNeuron1Layer)) - 1) *strength
        self.weights3 = (2 * np.random.random((self.noOfOutputs, self.noOfNeuron2Layer)) - 1) * strength

        self.bias1 = (2 * np.random.random((self.noOfInputs, 1)) - 1) * strength
        self.bias2 = (2 * np.random.random((self.noOfNeuron1Layer, 1)) - 1) * strength
        self.bias3 = (2 * np.random.random((self.noOfNeuron2Layer, 1)) - 1) * strength

        #print(self.weights1)
        #print(self.bias1)

    def exportWeight(self):
        rates = globalFcns.net2list(self.weights1, self.weights2, self.weights3, self.bias1, self.bias2, self.bias3)
        return rates

    def importWeight(self, rates):
        self.weights1, self.weights2, self.weights3, self.bias1, self.bias2, self.bias3 = globalFcns.list2net(self.weights1.shape,
                                                                                                              self.weights2.shape,
                                                                                                              self.weights3.shape,
                                                                                                              self.bias1.shape,
                                                                                                              self.bias2.shape,
                                                                                                              self.bias3.shape,
                                                                                                              rates)


    def think(self, input):
        self.inputs = np.array(input)[np.newaxis]
        outBias1 = np.add(self.inputs.T, self.bias1)

        outL1 = self.relu(outBias1)

        self.neuron1Layer = np.dot(self.weights1, outL1)
        outBias2 = np.add(self.neuron1Layer, self.bias2)

        outL2 = self.relu(outBias2)

        self.neuron2Layer = np.dot(self.weights2, outL2)
        outBias3 = np.add(self.neuron2Layer, self.bias3)

        outL3 = self.relu(outBias3)

        self.neuronLastLayer = np.dot(self.weights3, outL3)
        self.outputs = self.sigmoid(self.neuronLastLayer)

        maxElement = np.argmax(self.outputs)
        self.outputList = [0] * 4
        self.outputList[maxElement] = 1

        #self.outputList = [1, 0, 0, 0]

        #print(self.inputs)
        #print(self.outputs)
        #print(self.outputList)

    def sigmoid(self, input):
        return 1 / (1 + np.exp(-input))

    def silu(self, input):
        return input*self.sigmoid(input)

    def relu(self, input):
        return input * (input > 0)
    

