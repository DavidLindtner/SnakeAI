import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import threading
import csv
import sys
import time
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

from Globals import globalVars

from snakeBody import Snake

from Intelligence.generation import Generation

class AiScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AiScreen, self).__init__(**kwargs)
        self.generate = False
        self.noOfSnakes = 200
        self.noOfGenerations = 0
        self.snakes = []
        self.bestSnakes = []
        self.fitness = []
 
        self.graphName = 'data'

        self.cols = 1

        self.add_widget(Label(text='SNAKE AI'))

        numSnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        numSnakeLine.add_widget(Label(text='Number of snake\nin 1 generation', size_hint_x=None, width=200))
        self.noOfSnakesTI = TextInput(multiline=False, text=str(self.noOfSnakes), size_hint_x=None, width=50)
        numSnakeLine.add_widget(self.noOfSnakesTI)

        self.add_widget(numSnakeLine)

        num1SnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        num1SnakeLine.add_widget(Label(text='Selection rate', size_hint_x=None, width=200))
        self.selectionRateTI = TextInput(multiline=False, text=str(0.1), size_hint_x=None, width=50)
        num1SnakeLine.add_widget(self.selectionRateTI)

        self.add_widget(num1SnakeLine)

        num2SnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        num2SnakeLine.add_widget(Label(text='Mutation rate', size_hint_x=None, width=200))
        self.mutationRateTI = TextInput(multiline=False, text=str(0.01), size_hint_x=None, width=50)
        num2SnakeLine.add_widget(self.mutationRateTI)

        self.add_widget(num2SnakeLine)

        actualSnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        actualSnakeLine.add_widget(Label(text='Actual generation', size_hint_x=None, width=200))
        self.actualSnaleLabel = Label(text="0", size_hint_x=None, width=50)
        actualSnakeLine.add_widget(self.actualSnaleLabel)

        self.add_widget(actualSnakeLine)

        scoreSnakeLine = GridLayout(cols=5, row_force_default=True, row_default_height=30)
        scoreSnakeLine.add_widget(Label(text='Best score:', size_hint_x=None, width=100))
        self.scorelSnaleLabel = Label(text="0", size_hint_x=None, width=60)
        scoreSnakeLine.add_widget(self.scorelSnaleLabel)
        scoreSnakeLine.add_widget(Label(text=''))
        scoreSnakeLine.add_widget(Label(text='Best fitness:', size_hint_x=None, width=100))
        self.fitnesslSnaleLabel = Label(text="0", size_hint_x=None, width=60)
        scoreSnakeLine.add_widget(self.fitnesslSnaleLabel)

        self.add_widget(scoreSnakeLine)

        btn2Line = GridLayout(cols=5, rows=1, row_force_default=True, row_default_height=40)
        generateSnakesButton = Button(text="Generate Snakes", size_hint_x=None, width=150)
        generateSnakesButton.bind(on_press=self.generateSnakesButton)
        stopSnakeButton = Button(text="Stop generating", size_hint_x=None, width=150)
        stopSnakeButton.bind(on_press=self.stopSnakeButton)
        btn2Line.add_widget(Label())
        btn2Line.add_widget(generateSnakesButton)
        btn2Line.add_widget(Label())
        btn2Line.add_widget(stopSnakeButton)
        btn2Line.add_widget(Label())
        self.add_widget(btn2Line)

        graphsLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        graphsBut = Button(text="Show graphs", size_hint_x=None, width=100)
        graphsBut.bind(on_press=self.openGraphs)
        graphsLine.add_widget(Label())
        graphsLine.add_widget(graphsBut)
        graphsLine.add_widget(Label())
        self.add_widget(graphsLine)


        btn1Line = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        goStartBut = Button(text="Go back", size_hint_x=None, width=100)
        goStartBut.bind(on_press=self.goStartButton)
        btn1Line.add_widget(Label())
        btn1Line.add_widget(goStartBut)
        btn1Line.add_widget(Label())
        self.add_widget(btn1Line)


    def openGraphs(self, instance):
        from subprocess import Popen
        Popen(['python', 'graphs.py', str(self.graphName), '1'])


    def writeDataGraphs(self, score, gen, fit, sec):
        with open(self.graphName, 'a') as f:
            f.write(str(score) + ',' + str(gen) + ',' + str(fit) + ',' + str(sec) + ",\n")

    def goStartButton(self, instance):
        globalVars.screenManager.current = "Start"


    def generateSnakesButton(self, instance):
        if self.createDataCsv():
            self.generateThreadHandle = threading.Thread(target=self.generateThread, daemon=True)
            self.generateThreadHandle.start()


    def generateThread(self):
        self.noOfSnakes = int(self.noOfSnakesTI.text)

        self.generate = True

        bestSnakes = []
        self.bestScore = []
        self.bestFitness = []

        counterGen = 0
        startTime = time.time()

        while self.generate:
            if counterGen == 0:
                generation = Generation(noOfSnakes=self.noOfSnakes, selectionRate=float(self.selectionRateTI.text))
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
                generation = Generation(noOfSnakes=self.noOfSnakes, mutationRate=float(self.mutationRateTI.text), selectionRate=float(self.selectionRateTI.text))
                generation.live(parents=bestSnakes)
                bestSnakes = generation.exportBest()
                score, fitness = generation.bestScoreFitness()
                self.saveWeightsCsv(generation.bestWeights())
                actualTime = time.time() - startTime
                self.writeDataGraphs(score, counterGen, fitness, actualTime)
                del generation

            self.bestScore.append(score)
            self.bestFitness.append(fitness)

            self.actualSnaleLabel.text = str(counterGen)
            self.scorelSnaleLabel.text = str(score)
            self.fitnesslSnaleLabel.text = str(fitness)
            counterGen += 1

    def stopSnakeButton(self, instance):
        self.generate = False
        self.generateThreadHandle.join()
        self.saveBestScoreCsv()
        if os.path.exists(self.graphName):
            os.remove(self.graphName)

    def createDataCsv(self):
        now = datetime.now()
        self.fileDateTime = now.strftime("%d.%m.%Y-%H:%M:%S")
        initFileName = now.strftime("Population-%d-%m-%Y--%H-%M-%S")
        print(initFileName)
        self.fileName = filedialog.asksaveasfilename(initialdir="/", initialfile=initFileName, title="Export population", filetypes=(("CSV", "*.csv"), ("All files", "*.*")), defaultextension='.csv')
        if self.fileName:
            return True
        else:
            return False

    def saveDataCsv(self, noOfInputs, noOfNeuron1Layer, noOfNeuron2Layer):
        with open(self.fileName, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dateTime", self.fileDateTime])
            writer.writerow(["noOfSnakes", self.noOfSnakesTI.text])
            writer.writerow(["selectionRate", self.selectionRateTI.text])
            writer.writerow(["mutationRate", self.mutationRateTI.text])
            writer.writerow(["noOfInputs", noOfInputs])
            writer.writerow(["noOfNeuron1Layer", noOfNeuron1Layer])
            writer.writerow(["noOfNeuron2Layer", noOfNeuron2Layer])

    def saveWeightsCsv(self, weights):
        with open(self.fileName, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["weights", weights])

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

    def __del__(self):
        if os.path.exists(self.graphName):
            os.remove(self.graphName)