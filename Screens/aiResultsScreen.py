import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import tkinter as tk
from tkinter import filedialog

import csv

from Globals import globalVars

class AiResultScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AiResultScreen, self).__init__(**kwargs)
        
        self.cols = 1

        self.add_widget(Label(text='Result screen'))

        importLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        importBut = Button(text="Import population", size_hint_x=None, width=150)
        importBut.bind(on_press=self.importButton)
        importLine.add_widget(Label())
        importLine.add_widget(importBut)
        importLine.add_widget(Label())
        self.add_widget(importLine)


        dimLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        dimLine.add_widget(Label(text='Field dimensions', size_hint_x=None, width=200))
        self.fieldSizeTI = TextInput(multiline=False, text=str(globalVars.fieldSize-2), size_hint_x=None, width=50)
        dimLine.add_widget(self.fieldSizeTI)
        self.add_widget(dimLine)

        spdLine = GridLayout(cols=3, row_force_default=True, row_default_height=30)
        spdLine.add_widget(Label(text='Speed', size_hint_x=None, width=150))
        self.snakeSpeedTI = TextInput(multiline=False, text=str(globalVars.snakeSpeed), size_hint_x=None, width=50)
        spdLine.add_widget(self.snakeSpeedTI)
        spdLine.add_widget(Label(text='cell/s', size_hint_x=None, width=50))
        self.add_widget(spdLine)

        btnSimLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        simSnakeBut = Button(text="Simulate snake", size_hint_x=None, width=150)
        simSnakeBut.bind(on_press=self.simSnakeButton)
        btnSimLine.add_widget(Label())
        btnSimLine.add_widget(simSnakeBut)
        btnSimLine.add_widget(Label())
        self.add_widget(btnSimLine)

        btnLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        goStartBut = Button(text="Go back", size_hint_x=None, width=100)
        goStartBut.bind(on_press=self.goStartButton)
        btnLine.add_widget(Label())
        btnLine.add_widget(goStartBut)
        btnLine.add_widget(Label())
        self.add_widget(btnLine)



    def goStartButton(self, instance):
        globalVars.screenManager.current = "Start"

    def simSnakeButton(self, instance):
        fieldSize = str(int(self.fieldSizeTI.text))
        snakeSpeed = str(float(self.snakeSpeedTI.text))

        from subprocess import Popen, PIPE
        process = Popen(['python', 'simulateSnake.py', fieldSize, snakeSpeed, self.fileName, str(self.numOfWeight-1)])


    def importButton(self, instance):
        root = tk.Tk()
        root.withdraw()

        self.fileName = filedialog.askopenfilename(initialdir="/", title="Import population", filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        endFileName = self.fileName[-24:]
        self.dateTimeLearning = endFileName[:20]

        self.readStatCsv(self.fileName)
        

    def readStatCsv(self, fileName):
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            lineCount = 0
            for row in csv_reader:
                if lineCount == 0:
                    self.noOfSnakes = row[1]
                elif lineCount == 1:
                    self.selectionRate = row[1]
                elif lineCount == 2:
                    self.mutationRate = row[1]
                elif lineCount == 3:
                    self.noOfInputs = row[1]
                elif lineCount == 4:
                    self.noOfNeuron1Layer = row[1]
                elif lineCount == 5:
                    self.noOfNeuron2Layer = row[1]
                
                if row[0] == 'bestScores':
                    self.bestScores = list(map(int, row[1][1:-1].split(',')))
                if row[0] == 'bestFitness':
                    self.bestFitness = list(map(int, row[1][1:-1].split(',')))

                lineCount += 1
            self.numOfWeight = lineCount - 8


