import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.slider import Slider

import threading
import tkinter as tk
from tkinter import filedialog
import csv

from Globals import globalVars




class AiResultScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AiResultScreen, self).__init__(**kwargs)

        self.noOfWeights = 0
        self.weightSimulate = 0
        
        self.cols = 1

        self.add_widget(Label(text='RESULT SCREEN'))
################################## IMPORT BUTTON #################################################################################
        importLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        importBut = Button(text="Import population", size_hint_x=None, width=150)
        importBut.bind(on_press=self.importButton)
        importLine.add_widget(Label())
        importLine.add_widget(importBut)
        importLine.add_widget(Label())
        self.add_widget(importLine)

################################## INFO LABELS #################################################################################
        infoGrid = GridLayout(cols=2, rows=3, row_force_default=True, row_default_height=30)
        infoGrid.add_widget(Label(text='Date of training:'))
        self.dateLabel = Label(text='')
        infoGrid.add_widget(self.dateLabel)

        snakeGrid = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        snakeGrid.add_widget(Label(text='Total snakes:'))
        self.allSnakesLabel = Label(text='', width=20)
        snakeGrid.add_widget(self.allSnakesLabel)
        infoGrid.add_widget(snakeGrid)

        snakeGrid2 = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        snakeGrid2.add_widget(Label(text='Snakes in 1 gen.:'))
        self.snakes1Label = Label(text='', width=20)
        snakeGrid2.add_widget(self.snakes1Label)
        infoGrid.add_widget(snakeGrid2)

        selGrid = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        selGrid.add_widget(Label(text='Select. rate:'))
        self.selectionLabel = Label(text='')
        selGrid.add_widget(self.selectionLabel)
        infoGrid.add_widget(selGrid)

        mutGrid = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        mutGrid.add_widget(Label(text='Mutation rate:'))
        self.mutationLabel = Label(text='')
        mutGrid.add_widget(self.mutationLabel)
        infoGrid.add_widget(mutGrid)

        self.add_widget(infoGrid)

################################## SHOW GRAPHS #################################################################################
        btnGraphLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        graphBut = Button(text="Show graphs", size_hint_x=None, width=150)
        graphBut.bind(on_press=self.openGraphs)
        btnGraphLine.add_widget(Label())
        btnGraphLine.add_widget(graphBut)
        btnGraphLine.add_widget(Label())
        self.add_widget(btnGraphLine)

################################## SLIDER #################################################################################
        sliderLine = GridLayout(cols=1, rows=3, row_force_default=True, row_default_height=30)

        sliderLine.add_widget(Label(text="Generations"))

        self.slider = Slider(min=0, max=0, value=25, orientation='horizontal', size_hint=(0.8, 1))
        self.slider.fbind('value', self.onChangeSliderValue)
        
        sliderUpLine = BoxLayout()
        sliderUpLine.add_widget(Label(text='0', size_hint=(0.1, 1)))
        sliderUpLine.add_widget(self.slider)
        self.noOfWeightsLabel = Label(text='0', size_hint=(0.1, 1))
        sliderUpLine.add_widget(self.noOfWeightsLabel)
        sliderLine.add_widget(sliderUpLine)

        self.actSliderValLabel = Label(text='0')
        sliderLine.add_widget(self.actSliderValLabel)
        self.add_widget(sliderLine)

################################## FIELD DIMENSIONS SPEED #################################################################################
        dimLine = GridLayout(cols=3, rows=2, row_force_default=True, row_default_height=30, spacing=3)
        dimLine.add_widget(Label(text='Field dimensions', size_hint_x=None, width=200))
        self.fieldSizeTI = TextInput(multiline=False, text=str(globalVars.fieldSize-2), size_hint_x=None, width=50)
        dimLine.add_widget(self.fieldSizeTI)
        dimLine.add_widget(Label(text='cells', size_hint_x=None, width=50))

        dimLine.add_widget(Label(text='Speed', size_hint_x=None, width=200))
        self.snakeSpeedTI = TextInput(multiline=False, text=str(globalVars.snakeSpeed), size_hint_x=None, width=50)
        dimLine.add_widget(self.snakeSpeedTI)
        dimLine.add_widget(Label(text='cell/s', size_hint_x=None, width=50))
        self.add_widget(dimLine)

################################## SIMULATE SNAKE #################################################################################
        btnSimLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        simSnakeBut = Button(text="Simulate snake", size_hint_x=None, width=150)
        simSnakeBut.bind(on_press=self.simSnakeButton)
        btnSimLine.add_widget(Label())
        btnSimLine.add_widget(simSnakeBut)
        btnSimLine.add_widget(Label())
        self.add_widget(btnSimLine)

################################## GO BACK #################################################################################
        btnLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        goStartBut = Button(text='Go back', size_hint_x=None, width=150)
        goStartBut.bind(on_press=self.goStartButton)
        btnLine.add_widget(Label())
        btnLine.add_widget(goStartBut)
        btnLine.add_widget(Label())
        self.add_widget(btnLine)


    def onChangeSliderValue(self, instance, val):
        self.actSliderValLabel.text = str(int(val))
        self.weightSimulate = int(val)

    def goStartButton(self, instance):
        globalVars.screenManager.current = "Start"

    def simSnakeButton(self, instance):
        fieldSize = str(int(self.fieldSizeTI.text))
        snakeSpeed = str(float(self.snakeSpeedTI.text))
        from subprocess import Popen
        Popen(['python', 'simulateSnake.py', fieldSize, snakeSpeed, self.fileName, str(self.weightSimulate)])

    def importButton(self, instance):
        self.fileName = filedialog.askopenfilename(initialdir="/", title="Import population", filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        importThrHandle = threading.Thread(target=self.importThread, daemon=True)
        importThrHandle.start()

    def openGraphs(self, instance):
        from subprocess import Popen
        Popen(['python', 'graphs.py', str(self.fileName), '0'])


    def importThread(self):
        self.readStatCsv(self.fileName)
        self.updateInfo()

    def updateInfo(self):
        self.slider.max = self.noOfWeights
        self.noOfWeightsLabel.text = str(self.noOfWeights)

    def readStatCsv(self, fileName):
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            lineCount = 0
            self.noOfWeights = 0
            fileDateTime = ''
            noOfSnakes = ''
            selectionRate = ''
            mutationRate = ''
            for row in csv_reader:
                if lineCount == 0:
                    fileDateTime = row[1]
                elif lineCount == 1:
                    noOfSnakes = row[1]
                elif lineCount == 2:
                    selectionRate = row[1]
                elif lineCount == 3:
                    mutationRate = row[1]
                elif lineCount == 4:
                    self.noOfInputs = row[1]
                elif lineCount == 5:
                    self.noOfNeuron1Layer = row[1]
                elif lineCount == 6:
                    self.noOfNeuron2Layer = row[1]
                if row[0] == 'weights':
                    self.noOfWeights += 1
                lineCount += 1

            self.noOfWeights -= 1
            self.dateLabel.text = fileDateTime
            self.snakes1Label.text = noOfSnakes
            self.allSnakesLabel.text = str(int(noOfSnakes) * int(self.noOfWeights))
            self.selectionLabel.text = selectionRate
            self.mutationLabel.text = mutationRate




