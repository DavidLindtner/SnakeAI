import multiprocessing
import time

import threading
import csv
import sys
import time
import os
import sys

from datetime import datetime

from Globals import globalVars

from snakeBody import Snake

from Intelligence.generation import Generation

from Processes.graphProcess import GraphProcess

from kivy.core.window import Window


class GenProcess(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

        self.graphName = 'data'

    def run(self):
        globalVars.init()
        Window.hide()
        self.noOfSnakes, self.selectionRate, self.mutationRate, self.noOfNeuron1Layer, self.noOfNeuron2Layer, self.fileName, self.fileDateTime, fieldSize = self.task_queue.get()
        globalVars.fieldSize = fieldSize
        self.task_queue.task_done()
        self.result_queue.put(1)
        generate = 1

        bestSnakes = []
        self.bestScore = []
        self.bestFitness = []

        counterGen = 0
        startTime = 0
        while generate:
            generate = self.task_queue.get()
            if counterGen == 0:
                generation = Generation(noOfSnakes=self.noOfSnakes*10,
                                        selectionRate=self.selectionRate/10,
                                        noNeuron1Layer=self.noOfNeuron1Layer,
                                        noNeuron2Layer=self.noOfNeuron2Layer)
                startTime = time.time()
                generation.live()
                bestSnakes = generation.exportBest()
                score, fitness = generation.bestScoreFitness()
                noOfInputs, noOfNeuron1Layer, noOfNeuron2Layer = bestSnakes[0].exportDimBrain()
                self.saveDataCsv(noOfInputs=noOfInputs, noOfNeuron1Layer=noOfNeuron1Layer, noOfNeuron2Layer=noOfNeuron2Layer)
                self.saveWeightsCsv(generation.bestWeights())
                actualTime = time.time() - startTime
                self.writeDataGraphs(score, counterGen, fitness, actualTime)
                self.openGraphs(0)
                del generation
            else:
                generation = Generation(noOfSnakes=self.noOfSnakes,
                                        selectionRate=self.selectionRate,
                                        noNeuron1Layer=self.noOfNeuron1Layer,
                                        noNeuron2Layer=self.noOfNeuron2Layer,
                                        mutationRate=self.mutationRate)
                generation.live(parents=bestSnakes)
                bestSnakes = generation.exportBest()
                score, fitness = generation.bestScoreFitness()
                self.saveWeightsCsv(generation.bestWeights())
                actualTime = time.time() - startTime
                self.writeDataGraphs(score, counterGen, fitness, actualTime)
                del generation

            self.bestScore.append(score)
            self.bestFitness.append(fitness)

            counterGen += 1


            self.task_queue.task_done()
            self.result_queue.put([counterGen, score, fitness])


        self.saveBestScoreCsv()
        if os.path.exists(self.graphName):
            os.remove(self.graphName)

    def saveDataCsv(self, noOfInputs, noOfNeuron1Layer, noOfNeuron2Layer):
        with open(self.fileName, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dateTime", self.fileDateTime])
            writer.writerow(["noOfSnakes", str(self.noOfSnakes)])
            writer.writerow(["selectionRate", str(self.selectionRate)])
            writer.writerow(["mutationRate", str(self.mutationRate)])
            writer.writerow(["noOfInputs", noOfInputs])
            writer.writerow(["noOfNeuron1Layer", noOfNeuron1Layer])
            writer.writerow(["noOfNeuron2Layer", noOfNeuron2Layer])

    def saveWeightsCsv(self, weights):
        with open(self.fileName, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["weights", weights])


    def writeDataGraphs(self, score, gen, fit, sec):
        with open(self.graphName, 'a') as f:
            f.write(str(score) + ',' + str(gen) + ',' + str(fit) + ',' + str(sec) + ",\n")


    def saveBestScoreCsv(self):
        with open(self.graphName, "r") as file:
            self.score = []
            self.generation = []
            self.fitness = []
            self.seconds = []
            for line in file:
                data = list(line.split(","))
                score = int(data[0])
                generation = int(data[1])
                fitness = int(data[2])
                seconds = float(data[3])

                self.score.append(score)
                self.generation.append(generation)
                self.fitness.append(fitness)
                self.seconds.append(seconds)

        with open(self.fileName, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["score", self.score])
            writer.writerow(["generation", self.generation])
            writer.writerow(["fitness", self.fitness])
            writer.writerow(["seconds", self.seconds])


    def openGraphs(self, instance):
        openG = threading.Thread(target=self.openGraphsThr)
        openG.start()

    def openGraphsThr(self):
        dataIn = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        proces = GraphProcess(dataIn, results)
        proces.start()
        dataIn.put([self.graphName, 1])

