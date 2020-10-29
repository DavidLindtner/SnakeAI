import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image  
from kivy.lang import Builder 
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import SlideTransition

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


class ImageButton(ButtonBehavior, Image):  
    def on_press(self):
        globalVars.ScreenManager.transition = SlideTransition(direction='right')
        globalVars.screenManager.current = "Start"

Builder.load_string("""  
<ImageButton>:  
    source:'Icons/back.png'  
    size_hint: 0.05, 0.05
""")  

class AiScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AiScreen, self).__init__(**kwargs)
        self.generate = False
        self.noOfSnakes = 200
        self.noOfGenerations = 0
        self.noOfNeuron1Layer = 18
        self.noOfNeuron2Layer = 12
        self.snakes = []
        self.bestSnakes = []
        self.fitness = []
 
        self.graphName = 'data'

        self.cols = 1
############################## BACK TITLE ###########################################################################
        topLine = BoxLayout(orientation='horizontal', spacing=10)
        topLine.add_widget(Label(text='', size_hint=(0.05, 1)))
        topLine.add_widget(ImageButton(size_hint=(.1, 1)))
        topLine.add_widget(Label(text='SNAKE AI', size_hint=(.7, 1)))
        topLine.add_widget(Label(text='', size_hint=(0.15, 1)))
        self.add_widget(topLine)

############################## NUMBER OF SNAKES ###########################################################################
        numSnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        numSnakeLine.add_widget(Label(text='Number of snake\nin 1 generation', size_hint_x=None, width=200))
        self.noOfSnakesTI = TextInput(multiline=False, text=str(self.noOfSnakes), size_hint_x=None, width=50)
        numSnakeLine.add_widget(self.noOfSnakesTI)

        self.add_widget(numSnakeLine)

############################## SELECTION RATE ###########################################################################
        num1SnakeLine = GridLayout(cols=4, row_force_default=True, row_default_height=30)
        num1SnakeLine.add_widget(Label(text='Selection rate', size_hint_x=None, width=150))
        self.selectionRateTI = TextInput(multiline=False, text=str(0.1), size_hint_x=None, width=40)
        num1SnakeLine.add_widget(self.selectionRateTI)

        num1SnakeLine.add_widget(Label(text='Mutation rate', size_hint_x=None, width=150))
        self.mutationRateTI = TextInput(multiline=False, text=str(0.01), size_hint_x=None, width=40)
        num1SnakeLine.add_widget(self.mutationRateTI)

        self.add_widget(num1SnakeLine)

############################## MUTATION RATE ###########################################################################
        netSnakeLine = GridLayout(cols=4, row_force_default=True, row_default_height=30)
        netSnakeLine.add_widget(Label(text='Neurons in\n   1. layer', size_hint_x=None, width=150))
        self.neuron1LayerTI = TextInput(multiline=False, text=str(self.noOfNeuron1Layer), size_hint_x=None, width=40)
        netSnakeLine.add_widget(self.neuron1LayerTI)

        netSnakeLine.add_widget(Label(text='Neurons in\n   2. layer', size_hint_x=None, width=150))
        self.neuron2LayerTI = TextInput(multiline=False, text=str(self.noOfNeuron2Layer), size_hint_x=None, width=40)
        netSnakeLine.add_widget(self.neuron2LayerTI)

        self.add_widget(netSnakeLine)

############################## BUTTONS ###########################################################################
        btn2Line = GridLayout(cols=5, rows=1, row_force_default=True, row_default_height=40)
        generateSnakesButton = Button(text="Generate Snakes", size_hint_x=None, width=150)
        generateSnakesButton.bind(on_press=self.generateSnakesButton)
        self.stopSnakeBut = Button(text="Stop generating", size_hint_x=None, width=150, background_color =(1, 0, 0, 0.5))
        self.stopSnakeBut.bind(on_press=self.stopSnakeButton)
        btn2Line.add_widget(Label())
        btn2Line.add_widget(generateSnakesButton)
        btn2Line.add_widget(Label())
        btn2Line.add_widget(self.stopSnakeBut)
        btn2Line.add_widget(Label())
        self.add_widget(btn2Line)

############################## ACTUAL GENERATION ###########################################################################
        trainingInfoGrid = GridLayout(cols=1,row_force_default=True, row_default_height=30)

        actualSnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        actualSnakeLine.add_widget(Label(text='Actual generation', size_hint_x=None, width=200))
        self.actualSnaleLabel = Label(text="0", size_hint_x=None, width=50)
        actualSnakeLine.add_widget(self.actualSnaleLabel)

        trainingInfoGrid.add_widget(actualSnakeLine)

############################## SCORE FITNESS ###########################################################################
        scoreSnakeLine = GridLayout(cols=5, row_force_default=True, row_default_height=30)
        scoreSnakeLine.add_widget(Label(text='Best fitness:', size_hint_x=None, width=100))
        self.fitnesslSnaleLabel = Label(text="0", size_hint_x=None, width=60)
        scoreSnakeLine.add_widget(self.fitnesslSnaleLabel)
        scoreSnakeLine.add_widget(Label(text=''))
        scoreSnakeLine.add_widget(Label(text='Best score:', size_hint_x=None, width=100))
        self.scorelSnaleLabel = Label(text="0", size_hint_x=None, width=60)
        scoreSnakeLine.add_widget(self.scorelSnaleLabel)
        trainingInfoGrid.add_widget(scoreSnakeLine)

        self.add_widget(trainingInfoGrid)

############################## SHOW GRAPHS ###########################################################################
        graphsLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        graphsBut = Button(text="Show graphs", size_hint_x=None, width=150)
        graphsBut.bind(on_press=self.openGraphs)
        graphsLine.add_widget(Label())
        graphsLine.add_widget(graphsBut)
        graphsLine.add_widget(Label())
        self.add_widget(graphsLine)


    def openGraphs(self, instance):
        if self.generate == 0:
            self.popupGraphsShow()
        else:
            from subprocess import Popen
            Popen(['python', 'graphs.py', str(self.graphName), '1'])


    def writeDataGraphs(self, score, gen, fit, sec):
        with open(self.graphName, 'a') as f:
            f.write(str(score) + ',' + str(gen) + ',' + str(fit) + ',' + str(sec) + ",\n")

    def generateSnakesButton(self, instance):
        self.noOfNeuron1Layer = int(self.neuron1LayerTI.text)
        self.noOfNeuron2Layer = int(self.neuron2LayerTI.text)

        if self.createDataCsv():
            self.stopSnakeBut.background_color = [1, 0.3, 0.3, 1]
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
                generation = Generation(noOfSnakes=self.noOfSnakes,
                                        selectionRate=float(self.selectionRateTI.text),
                                        noNeuron1Layer=self.noOfNeuron1Layer,
                                        noNeuron2Layer=self.noOfNeuron2Layer)
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
                                        selectionRate=float(self.selectionRateTI.text),
                                        noNeuron1Layer=self.noOfNeuron1Layer,
                                        noNeuron2Layer=self.noOfNeuron2Layer,
                                        mutationRate=float(self.mutationRateTI.text))
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
        if self.generate == True:
            self.stopSnakeBut.background_color = [1, 0, 0, 0.5]       
            self.generate = False
            self.generateThreadHandle.join()
            self.saveBestScoreCsv()
            if os.path.exists(self.graphName):
                os.remove(self.graphName)

    def createDataCsv(self):
        now = datetime.now()
        self.fileDateTime = now.strftime("%d.%m.%Y-%H:%M:%S")
        initFileName = now.strftime("Population-%d-%m-%Y--%H-%M-%S")
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


    def popupGraphsShow(self):
        layout = GridLayout(cols = 1, padding = 10) 
        popupLabel1 = Label(text = "Training has not started") 
        popupLabel2 = Label(text = "NO graphs for training available") 
        layout.add_widget(popupLabel1) 
        layout.add_widget(popupLabel2) 
        popup = Popup(title ='INFO', 
                        content = layout, 
                        size_hint =(None, None), size =(300, 150))   
        popup.open()     

    def __del__(self):
        if os.path.exists(self.graphName):
            os.remove(self.graphName)