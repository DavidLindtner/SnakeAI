import numpy as np
from snakeBody import Snake
from Globals import globalFcns

class Crossover():
    def __init__(self, inSnakes, noOfOutSnakes, mutationRate, noNeuron1Layer, noNeuron2Layer):
        self.noOfNeuron1Layer = noNeuron1Layer
        self.noOfNeuron2Layer = noNeuron2Layer
        self.mutationRate = mutationRate
        self.inSnakes = inSnakes
        self.noOutSnakes = noOfOutSnakes
        self.outSnakes = []


    def simpleCrossover(self):
        numOffsprigns = int(self.noOutSnakes/len(self.inSnakes))
        offspringsList = [numOffsprigns] * len(self.inSnakes)
        i = 0
        while sum(offspringsList) < self.noOutSnakes:
            offspringsList[i] += 1
            i += 1

        for i in range(len(offspringsList)):
            for j in range(offspringsList[i]-1):
                ratesOld = self.inSnakes[i].exportBrain()
                ratesNew = self.mutation(ratesOld)
                self.outSnakes.append(Snake(intelligence=True))
                self.outSnakes[-1].importBrain(ratesNew, noOfNeuron1=self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)
            
            ratesOld = self.inSnakes[i].exportBrain()
            self.outSnakes.append(Snake(intelligence=True))
            self.outSnakes[-1].importBrain(ratesOld, noOfNeuron1=self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)

        return self.outSnakes



    def onePointCrossover(self):
        if len(self.inSnakes) % 2 == 1:
            self.inSnakes.insert(0, self.inSnakes[0])

        ratesOffspringList = []

        inSnake = self.inSnakes.copy()

        while inSnake:
            index1 = np.random.randint(len(inSnake))
            parent1 = inSnake[index1]
            inSnake.pop(index1)

            index2 = np.random.randint(len(inSnake))
            parent2 = inSnake[index2]
            inSnake.pop(index2)

            rates1 = []
            rates2 = []
            ratesOffspring = []

            rates1 = parent1.exportBrain()
            rates2 = parent2.exportBrain()

            randSpot = np.random.randint(len(rates1))

            ratesOffspring = rates1[:randSpot] + rates2[randSpot:]
            ratesOffspringList.append(ratesOffspring)


        numOffsprigns = int(self.noOutSnakes/len(ratesOffspringList))
        offspringsList = [numOffsprigns] * len(ratesOffspringList)

        i = 0
        while sum(offspringsList) < self.noOutSnakes:
            offspringsList[i] += 1
            i += 1

        for i in range(len(offspringsList)):
            for j in range(offspringsList[i] - 2):
                ratesOld = ratesOffspringList[i].copy()
                ratesNew = self.mutation(ratesOld)
                self.outSnakes.append(Snake(intelligence=True))
                self.outSnakes[-1].importBrain(ratesNew, noOfNeuron1=self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)

        for i in range(len(self.inSnakes)):
            ratesOld = self.inSnakes[i].exportBrain()
            self.outSnakes.append(Snake(intelligence=True))
            self.outSnakes[-1].importBrain(ratesOld, noOfNeuron1=self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)

        return self.outSnakes


    def twoPointCrossover(self):
        if len(self.inSnakes) % 2 == 1:
            self.inSnakes.insert(0, self.inSnakes[0])

        ratesOffspringList = []

        inSnake = self.inSnakes.copy()

        while inSnake:
            index1 = np.random.randint(len(inSnake))
            parent1 = inSnake[index1]
            inSnake.pop(index1)

            index2 = np.random.randint(len(inSnake))
            parent2 = inSnake[index2]
            inSnake.pop(index2)

            rates1 = []
            rates2 = []
            ratesOffspring = []

            rates1 = parent1.exportBrain()
            rates2 = parent2.exportBrain()

            randSpots = [np.random.randint(len(rates1)), np.random.randint(len(rates1)), np.random.randint(len(rates1))]
            randSpots.sort()

            ratesOffspring = rates1[:randSpots[0]] + rates2[randSpots[0]:randSpots[1]] + rates1[randSpots[1]:randSpots[2]] + rates2[randSpots[0]:]
            ratesOffspringList.append(ratesOffspring)


        numOffsprigns = int(self.noOutSnakes/len(ratesOffspringList))
        offspringsList = [numOffsprigns] * len(ratesOffspringList)

        i = 0
        while sum(offspringsList) < self.noOutSnakes:
            offspringsList[i] += 1
            i += 1

        for i in range(len(offspringsList)):
            for j in range(offspringsList[i] - 2):
                ratesOld = ratesOffspringList[i].copy()
                ratesNew = self.mutation(ratesOld)
                self.outSnakes.append(Snake(intelligence=True))
                self.outSnakes[-1].importBrain(ratesNew, noOfNeuron1=self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)

        for i in range(len(self.inSnakes)):
            ratesOld = self.inSnakes[i].exportBrain()
            self.outSnakes.append(Snake(intelligence=True))
            self.outSnakes[-1].importBrain(ratesOld, noOfNeuron1=self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)

        return self.outSnakes


    def mutation(self, Rates):
        mutationStrength = 0.15
        for i in range(int(len(Rates) * self.mutationRate)):
            x = np.random.randint(len(Rates))
            Rates[x] += (2 * np.random.random() - 1) * mutationStrength

        for i in range(int(len(Rates) * self.mutationRate / 5)):
            x = np.random.randint(len(Rates))
            Rates[x] += (2 * np.random.random() - 1) * mutationStrength * 5

        for i in range(int(len(Rates) * self.mutationRate / 10)):
            x = np.random.randint(len(Rates))
            Rates[x] += (2 * np.random.random() - 1) * mutationStrength * 10

        return Rates