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
import multiprocessing
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

from Processes.generationProcess import GenProcess

from Processes.graphProcess import GraphProcess

from Processes.simulateProcess import SimulateProcess

class ImageButton(ButtonBehavior, Image):  
    def on_press(self):
        globalVars.ScreenManager.transition = SlideTransition(direction='left')
        globalVars.screenManager.current = "Start"

Builder.load_string("""  
<ImageButton>:  
    source:'Icons/front.png'  
    size_hint: 0.05, 0.05
""")  

class AiScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AiScreen, self).__init__(**kwargs)
        self.generate = False
        self.noOfSnakes = 200
        self.noOfGenerations = 0
        self.noOfNeuron1Layer = 30
        self.noOfNeuron2Layer = 15
        self.snakes = []
        self.bestSnakes = []
        self.fitness = []
 
        self.graphName = 'data'

        self.cols = 1
############################## BACK TITLE ###########################################################################
        topLine = BoxLayout(orientation='horizontal', spacing=10)
        topLine.add_widget(Label(text='', size_hint=(0.15, 1)))
        topLine.add_widget(Label(text='AI SETUP', size_hint=(.7, 1), font_size='30sp'))
        topLine.add_widget(ImageButton(source='Icons/front.png', size_hint=(.1, 1)))
        topLine.add_widget(Label(text='', size_hint=(0.05, 1)))
        self.add_widget(topLine)

############################## NUMBER OF SNAKES ###########################################################################
        numSnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        numSnakeLine.add_widget(Label(text='Number of snakes\n   in 1 generation', size_hint_x=None, width=250, font_size='20sp'))
        self.noOfSnakesTI = TextInput(multiline=False, text=str(self.noOfSnakes), size_hint_x=None, width=70, font_size='20sp')
        numSnakeLine.add_widget(self.noOfSnakesTI)

        self.add_widget(numSnakeLine)

############################## SELECTION RATE ###########################################################################
        num1SnakeLine = GridLayout(cols=4, row_force_default=True, row_default_height=40)
        num1SnakeLine.add_widget(Label(text='Selection rate', size_hint_x=None, width=150, font_size='20sp'))
        self.selectionRateTI = TextInput(multiline=False, text=str(0.1), size_hint_x=None, width=50, font_size='20sp')
        num1SnakeLine.add_widget(self.selectionRateTI)

        num1SnakeLine.add_widget(Label(text='Mutation rate', size_hint_x=None, width=150, font_size='20sp'))
        self.mutationRateTI = TextInput(multiline=False, text=str(0.05), size_hint_x=None, width=50, font_size='20sp')
        num1SnakeLine.add_widget(self.mutationRateTI)

        self.add_widget(num1SnakeLine)

############################## MUTATION RATE ###########################################################################
        netSnakeLine = GridLayout(cols=4, row_force_default=True, row_default_height=40)
        netSnakeLine.add_widget(Label(text='Neurons in\n   1. layer', size_hint_x=None, width=150, font_size='20sp'))
        self.neuron1LayerTI = TextInput(multiline=False, text=str(self.noOfNeuron1Layer), size_hint_x=None, width=50, font_size='20sp')
        netSnakeLine.add_widget(self.neuron1LayerTI)

        netSnakeLine.add_widget(Label(text='Neurons in\n   2. layer', size_hint_x=None, width=150, font_size='20sp'))
        self.neuron2LayerTI = TextInput(multiline=False, text=str(self.noOfNeuron2Layer), size_hint_x=None, width=50, font_size='20sp')
        netSnakeLine.add_widget(self.neuron2LayerTI)

        self.add_widget(netSnakeLine)

############################## BUTTONS ###########################################################################
        btn2Line = GridLayout(cols=5, rows=1, row_force_default=True, row_default_height=50)
        generateSnakesButton = Button(text="Generate Snakes", size_hint_x=None, width=200, font_size='20sp')
        generateSnakesButton.bind(on_press=self.generateSnakesButton)
        self.stopSnakeBut = Button(text="Stop generating", size_hint_x=None, width=200, background_color =(1, 0, 0, 0.5), font_size='20sp')
        self.stopSnakeBut.bind(on_press=self.stopSnakeButton)
        btn2Line.add_widget(Label())
        btn2Line.add_widget(generateSnakesButton)
        btn2Line.add_widget(Label())
        btn2Line.add_widget(self.stopSnakeBut)
        btn2Line.add_widget(Label())
        self.add_widget(btn2Line)

############################## ACTUAL GENERATION ###########################################################################
        trainingInfoGrid = GridLayout(cols=1,row_force_default=True, row_default_height=40)

        actualSnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        actualSnakeLine.add_widget(Label(text='Actual generation', size_hint_x=None, width=250, font_size='20sp'))
        self.actualSnaleLabel = Label(text="0", size_hint_x=None, width=50, font_size='20sp')
        actualSnakeLine.add_widget(self.actualSnaleLabel)

        trainingInfoGrid.add_widget(actualSnakeLine)

############################## SCORE FITNESS ###########################################################################
        scoreSnakeLine = GridLayout(cols=5, row_force_default=True, row_default_height=40)
        scoreSnakeLine.add_widget(Label(text='Best fitness:', size_hint_x=None, width=150, font_size='20sp'))
        self.fitnesslSnaleLabel = Label(text="0", size_hint_x=None, width=60, font_size='20sp')
        scoreSnakeLine.add_widget(self.fitnesslSnaleLabel)
        scoreSnakeLine.add_widget(Label())
        scoreSnakeLine.add_widget(Label(text='Best score:', size_hint_x=None, width=150, font_size='20sp'))
        self.scorelSnaleLabel = Label(text="0", size_hint_x=None, width=60, font_size='20sp')
        scoreSnakeLine.add_widget(self.scorelSnaleLabel)
        trainingInfoGrid.add_widget(scoreSnakeLine)

        self.add_widget(trainingInfoGrid)

############################## SHOW GRAPHS ###########################################################################
        btn1Line = GridLayout(cols=5, rows=1, row_force_default=True, row_default_height=50)
        graphsBut = Button(text="Show graphs", size_hint_x=None, width=200, font_size='20sp')
        graphsBut.bind(on_press=self.openGraphs)
        simulateBut = Button(text="Run actual snake", size_hint_x=None, width=200, font_size='20sp')
        simulateBut.bind(on_press=self.simulateSnake)
        btn1Line.add_widget(Label())
        btn1Line.add_widget(graphsBut)
        btn1Line.add_widget(Label())
        btn1Line.add_widget(simulateBut)
        btn1Line.add_widget(Label())
        self.add_widget(btn1Line)


    def openGraphs(self, instance):
        if self.generate == 0:
            self.popupShow(0)
        else:
            openG = threading.Thread(target=self.openGraphsThr)
            openG.start()

    def simulateSnake(self, instance):
        if self.generate == 0:
            self.popupShow(1)
        else:
            openG = threading.Thread(target=self.simulateSnakeThr)
            openG.start()

    def openGraphsThr(self):
        dataIn = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        proces = GraphProcess(dataIn, results)
        proces.start()
        dataIn.put([self.graphName, 1])

    def simulateSnakeThr(self):
        dataIn = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        proces = SimulateProcess(dataIn, results)
        proces.start()
        dataIn.put([globalVars.fieldSize, 50, self.fileName, int(self.actualSnaleLabel.text)])

    def generateSnakesButton(self, instance):
        if self.generate:
            self.popupShow(2)
        else:
            if os.path.exists(self.graphName):
                os.remove(self.graphName)
                
            self.noOfNeuron1Layer = int(self.neuron1LayerTI.text)
            self.noOfNeuron2Layer = int(self.neuron2LayerTI.text)
            self.noOfSnakes = int(self.noOfSnakesTI.text)

            if self.createDataCsv():
                self.stopSnakeBut.background_color = [1, 0.3, 0.3, 1]

                self.generateProcessHandle = threading.Thread(target=self.generateProcessThread, daemon=True)
                self.generateProcessHandle.start()

    def generateProcessThread(self):
        dataIn = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        multiprocessing.freeze_support()        
        gen = GenProcess(dataIn, results)
        gen.start()
        
        
        dataIn.put([self.noOfSnakes, float(self.selectionRateTI.text), float(self.mutationRateTI.text), self.noOfNeuron1Layer, self.noOfNeuron2Layer, self.fileName, self.fileDateTime, globalVars.fieldSize])
        result = results.get()

        self.generate = True
        while self.generate:
            dataIn.put(1)
            result = results.get()           
            self.actualSnaleLabel.text = str(result[0])
            self.scorelSnaleLabel.text = str(result[1])
            self.fitnesslSnaleLabel.text = str(result[2])

        dataIn.put(0)


    def stopSnakeButton(self, instance):
        stopGenerateHandle = threading.Thread(target=self.stopGenerateThread, daemon=True)
        stopGenerateHandle.start()

    def stopGenerateThread(self):
        if self.generate == True:
            self.stopSnakeBut.text = "Stopping"
            self.generate = False
            self.generateProcessHandle.join()
            self.stopSnakeBut.background_color = [1, 0, 0, 0.5] 
            self.stopSnakeBut.text = "Stop generating"

    def createDataCsv(self):
        now = datetime.now()
        self.fileDateTime = now.strftime("%Y.%m.%d-%H:%M:%S")
        initFileName = now.strftime("Population-%Y-%m-%d--%H-%M-%S")
        self.fileName = filedialog.asksaveasfilename(initialdir=globalVars.initialDir, initialfile=initFileName, title="Export population", filetypes=(("CSV", "*.csv"), ("All files", "*.*")), defaultextension='.csv')
        globalVars.initialDir = os.path.split(self.fileName)
        if self.fileName:
            return True
        else:
            return False


    def popupShow(self, info):
        layout = GridLayout(cols = 1, padding = 10) 
        if info == 0:
            popupLabel1 = Label(text = "Training has not started", font_size='20sp')
            popupLabel2 = Label(text = "NO graphs for training available", font_size='20sp')
        elif info == 1:
            popupLabel1 = Label(text = "Training has not started", font_size='20sp')
            popupLabel2 = Label(text = "NO simulations for training available", font_size='20sp')
        elif info == 2:
            popupLabel1 = Label(text = "Training is running", font_size='20sp')
            popupLabel2 = Label(text = "Stop the training and train again", font_size='20sp')

        layout.add_widget(popupLabel1) 
        layout.add_widget(popupLabel2) 
        popup = Popup(title ='INFO',
                        content = layout, 
                        size_hint =(None, None), size =(400, 200))   
        popup.open()

    def __del__(self):
        if os.path.exists(self.graphName):
            os.remove(self.graphName)