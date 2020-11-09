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
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image  
from kivy.lang import Builder 
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import SlideTransition

import threading
import tkinter as tk
from tkinter import filedialog
import csv

from Globals import globalVars


class ImageButton(ButtonBehavior, Image):  
    def on_press(self):
        globalVars.ScreenManager.transition = SlideTransition(direction='right')
        globalVars.screenManager.current = "Start"

Builder.load_string("""  
<ImageButton>:  
    source:'Icons/back.png'  
    size_hint: 0.05, 0.05 
""")  

class AiResultScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AiResultScreen, self).__init__(**kwargs)

        self.noOfWeights = 0
        self.weightSimulate = 0
        self.fileName = ''
        self.cols = 1

        topLine = BoxLayout(orientation='horizontal', spacing=10)
        topLine.add_widget(Label(text='', size_hint=(0.05, 1)))
        topLine.add_widget(ImageButton(size_hint=(.1, 1)))
        topLine.add_widget(Label(text='RESULT SCREEN', size_hint=(.7, 1)))
        topLine.add_widget(Label(text='', size_hint=(0.15, 1)))
        self.add_widget(topLine)

################################## IMPORT BUTTON #################################################################################
        mainGrid = GridLayout(cols=1, row_force_default=True, row_default_height=30)

        importLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        importBut = Button(text="Import population", size_hint_x=None, width=150)
        importBut.bind(on_press=self.importButton)
        importLine.add_widget(Label())
        importLine.add_widget(importBut)
        importLine.add_widget(Label())
        mainGrid.add_widget(importLine)

        mainGrid.add_widget(Label())

################################## INFO LABELS #################################################################################
        infoGrid = GridLayout(cols=2, rows=8, row_force_default=True, row_default_height=15)
        infoGrid.add_widget(Label(text='Date of training:'))
        self.dateLabel = Label(text='')
        infoGrid.add_widget(self.dateLabel)

        infoGrid.add_widget(Label())
        infoGrid.add_widget(Label())

        snakeGrid = GridLayout(cols=3, row_force_default=True, row_default_height=30)
        snakeGrid.add_widget(Label(size_hint_x=None, width=10))
        snakeGrid.add_widget(Label(text='Total snakes:'))
        self.allSnakesLabel = Label(text='')
        snakeGrid.add_widget(self.allSnakesLabel)
        infoGrid.add_widget(snakeGrid)

        snakeGrid2 = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        snakeGrid2.add_widget(Label(text='Snakes in 1 gen.:'))
        self.snakes1Label = Label(text='')
        snakeGrid2.add_widget(self.snakes1Label)
        infoGrid.add_widget(snakeGrid2)

        infoGrid.add_widget(Label())
        infoGrid.add_widget(Label())

        selGrid = GridLayout(cols=3, row_force_default=True, row_default_height=30)
        selGrid.add_widget(Label(size_hint_x=None, width=10))
        selGrid.add_widget(Label(text='Select. rate:'))
        self.selectionLabel = Label(text='')
        selGrid.add_widget(self.selectionLabel)
        infoGrid.add_widget(selGrid)

        mutGrid = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        mutGrid.add_widget(Label(text='Mutation rate:'))
        self.mutationLabel = Label(text='')
        mutGrid.add_widget(self.mutationLabel)
        infoGrid.add_widget(mutGrid)

        infoGrid.add_widget(Label())
        infoGrid.add_widget(Label())
        infoGrid.add_widget(Label())
        infoGrid.add_widget(Label())

        net1Grid = GridLayout(cols=3, row_force_default=True, row_default_height=25)
        net1Grid.add_widget(Label(size_hint_x=None, width=10))
        net1Grid.add_widget(Label(text='Neurons in\n   1. layer:'))
        self.noNeuron1Label = Label(text='')
        net1Grid.add_widget(self.noNeuron1Label)
        infoGrid.add_widget(net1Grid)

        net2Grid = GridLayout(cols=2, row_force_default=True, row_default_height=25)
        net2Grid.add_widget(Label(text='Neurons in\n   2. layer:'))
        self.noNeuron2Label = Label(text='')
        net2Grid.add_widget(self.noNeuron2Label)
        infoGrid.add_widget(net2Grid)

        mainGrid.add_widget(infoGrid)

        self.add_widget(mainGrid)

        self.add_widget(Label())

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
        self.snakeSpeedTI = TextInput(multiline=False, text=str(100), size_hint_x=None, width=50)
        dimLine.add_widget(self.snakeSpeedTI)
        dimLine.add_widget(Label(text='cell/s', size_hint_x=None, width=50))
        self.add_widget(dimLine)

################################## SIMULATE SNAKE, SHOW GRAPHS #################################################################################
        btnSimLine = GridLayout(cols=5, rows=1, row_force_default=True, row_default_height=40)
        simSnakeBut = Button(text="Simulate snake", size_hint_x=None, width=150)
        simSnakeBut.bind(on_press=self.simSnakeButton)
        btnSimLine.add_widget(Label())
        btnSimLine.add_widget(simSnakeBut)
        btnSimLine.add_widget(Label())

        graphBut = Button(text="Show graphs", size_hint_x=None, width=150)
        graphBut.bind(on_press=self.openGraphs)
        btnSimLine.add_widget(graphBut)
        btnSimLine.add_widget(Label())
        self.add_widget(btnSimLine)


    def onChangeSliderValue(self, instance, val):
        self.actSliderValLabel.text = str(int(val))
        self.weightSimulate = int(val)

    def simSnakeButton(self, instance):
        if self.fileName == '':
            self.popupShow()
        else:
            simS = threading.Thread(target=self.simSnakeThr)
            simS.start()

    def simSnakeThr(self):
        fieldSize = str(int(self.fieldSizeTI.text))
        snakeSpeed = str(float(self.snakeSpeedTI.text))
        from subprocess import Popen
        if globalVars.executable:
            Popen(['simulateSnake.exe', fieldSize, snakeSpeed, self.fileName, str(self.weightSimulate)])
        else:
            Popen(['python', 'simulateSnake.py', fieldSize, snakeSpeed, self.fileName, str(self.weightSimulate)])


    def importButton(self, instance):
        self.fileName = filedialog.askopenfilename(initialdir="/", title="Import population", filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        if self.fileName:
            importThrHandle = threading.Thread(target=self.importThread, daemon=True)
            importThrHandle.start()


    def openGraphs(self, instance):
        if self.fileName == '':
            self.popupShow()
        else:
            openG = threading.Thread(target=self.openGraphsThr)
            openG.start()

    def openGraphsThr(self):
        from subprocess import Popen
        if globalVars.executable:
            Popen(['graphs.exe', str(self.fileName), '0'])
        else:
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
                    noOfInputs = row[1]
                elif lineCount == 5:
                    noOfNeuron1Layer = row[1]
                elif lineCount == 6:
                    noOfNeuron2Layer = row[1]
                if row[0] == 'weights':
                    self.noOfWeights += 1
                lineCount += 1

            self.noOfWeights -= 1
            self.dateLabel.text = fileDateTime
            self.snakes1Label.text = noOfSnakes
            self.allSnakesLabel.text = str(int(noOfSnakes) * int(self.noOfWeights))
            self.selectionLabel.text = selectionRate
            self.mutationLabel.text = mutationRate
            self.noNeuron1Label.text = noOfNeuron1Layer
            self.noNeuron2Label.text = noOfNeuron2Layer

    def popupShow(self):
        layout = GridLayout(cols = 1, padding = 10) 
        popupLabel1 = Label(text = "NO file selected") 
        popupLabel2 = Label(text = "IMPORT file with population of snakes") 
        layout.add_widget(popupLabel1) 
        layout.add_widget(popupLabel2) 
        popup = Popup(title ='INFO', 
                        content = layout, 
                        size_hint =(None, None), size =(300, 150))   
        popup.open()            




