import numpy as np

# outputs:
#   0   right
#   1   down
#   2   left
#   3   up

class Brain():
    def __init__(self, weight1=0, weight2=0, weight3=0):
        self.noOfInputs = 28
        self.noOfNeuron1Layer = 20
        self.noOfNeuron2Layer = 16
        self.noOfOutputs = 4

        self.inputs = np.ones((self.noOfInputs, 1))
        self.neuron1Layer = np.zeros((self.noOfNeuron1Layer, 1))
        self.neuron2Layer = np.zeros((self.noOfNeuron2Layer, 1))
        self.outputs = np.zeros((self.noOfOutputs, 1))
        self.outputList = [0] * 4


        #self.weights1 = np.zeros((self.noOfNeuron1Layer, self.noOfInputs))
        #self.weights2 = np.zeros((self.noOfNeuron2Layer, self.noOfNeuron1Layer))
        #self.weights3 = np.zeros((self.noOfOutputs, self.noOfNeuron2Layer))

        if weight1 == 0 and weight2 == 0 and weight3 == 0:
            self.randomWeights()
        else:
            self.mutate(w1=weight1, w2=weight2, w3=weight3)

    def mutate(self, w1, w2, w3):
        self.weights1 = w1
        self.weights2 = w2
        self.weights3 = w3

    def randomWeights(self):
        self.weights1 = 2 * np.random.random((self.noOfNeuron1Layer, self.noOfInputs)) - 1
        self.weights2 = 2 * np.random.random((self.noOfNeuron2Layer, self.noOfNeuron1Layer)) - 1
        self.weights3 = 2 * np.random.random((self.noOfOutputs, self.noOfNeuron2Layer)) - 1


    def think(self, input):
        self.inputs = np.array(input)
        self.neuron1Layer = np.dot(self.weights1, self.inputs)
        self.neuron2Layer = np.dot(self.weights2, self.neuron1Layer)
        self.outputs = self.sigmoid(np.dot(self.weights3, self.neuron2Layer))
        maxElement = np.argmax(self.outputs)
        self.outputList = [0] * 4
        self.outputList[maxElement] = 1

        print(self.inputs)
        print(self.outputList)

    def sigmoid(self, input):
        return 1 / (1 + np.exp(-input))


if __name__ == '__main__':

    brain = Brain()
    brain.think()
    

