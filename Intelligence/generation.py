import threading

from Globals import globalVars
from snakeBody import Snake

from Intelligence.selection import Selection
from Intelligence.crossover import Crossover


class Generation():
    def __init__(self, noOfSnakes, selectionRate, noNeuron1Layer, noNeuron2Layer, mutationRate=0):
        self.noOfThreads = 10

        self.noOfNeuron1Layer = noNeuron1Layer
        self.noOfNeuron2Layer = noNeuron2Layer

        self.noOfSnakes = noOfSnakes
        self.mutationRate = mutationRate
        self.selectionRate = selectionRate
        self.snakes = []
        self.fitness = [0] * self.noOfSnakes

    def live(self, parents=[]):
        if not parents:
            for i in range(self.noOfSnakes):
                self.snakes.append(Snake(intelligence=True))
                self.snakes[i].randomBrain(noOfNeuron1 = self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)
        else:
            cross = Crossover(inSnakes=parents.copy(), noOfOutSnakes=self.noOfSnakes, mutationRate=self.mutationRate, noNeuron1Layer=self.noOfNeuron1Layer, noNeuron2Layer=self.noOfNeuron2Layer)
            self.snakes = cross.onePointCrossover()
            del cross


        thrHandle = []
        for i in range(self.noOfThreads):
            arg1 = i * int(self.noOfSnakes/self.noOfThreads)
            arg2 = arg1 + int(self.noOfSnakes/self.noOfThreads)
            if i == self.noOfThreads-1:
                thrHandle.append(threading.Thread(target=self.simulateSnakeThr, args=(arg1, self.noOfSnakes,), daemon=True))
            else:
                thrHandle.append(threading.Thread(target=self.simulateSnakeThr, args=(arg1, arg2,), daemon=True))
          
        for thr in thrHandle:
            thr.start()

        for thr in thrHandle:
            thr.join()


    def simulateSnakeThr(self, start, stop):
        for j in range(start, stop):
            while True:
                if not self.snakes[j].snakeStep():  # if dead
                    self.fitness[j] = self.snakes[j].fitness
                    break

    def exportBest(self):
        selection = Selection()
        bestSnakesIndex = selection.selectBestRank(self.fitness.copy(), self.selectionRate)

        bestSnakes = []

        for bSnake in bestSnakesIndex:
            bestSnakes.append(self.snakes[bSnake])

        return bestSnakes

    def bestWeights(self):
        bestSnakeIndex = self.fitness.index(max(self.fitness))
        return self.snakes[bestSnakeIndex].exportBrain()

    def bestScoreFitness(self):
        bestSnakeIndex = self.fitness.index(max(self.fitness))
        return [self.snakes[bestSnakeIndex].score, self.fitness[bestSnakeIndex]]

    def __del__(self):
        for snake in self.snakes:
            del snake