import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import threading

import globalVars
from snakeBody import Snake

class AiScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AiScreen, self).__init__(**kwargs)
        self.generate = False
        self.noOfSnakes = 200
        self.noOfGenerations = 0
        self.snakes = []
 
        self.cols = 1

        self.add_widget(Label(text='SNAKE AI'))

        numSnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        numSnakeLine.add_widget(Label(text='Number of snake\nin 1 generation', size_hint_x=None, width=200))
        self.noOfSnakesTI = TextInput(multiline=False, text=str(self.noOfSnakes), size_hint_x=None, width=50)
        numSnakeLine.add_widget(self.noOfSnakesTI)

        self.add_widget(numSnakeLine)

        actualSnakeLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        actualSnakeLine.add_widget(Label(text='Actual generation', size_hint_x=None, width=200))
        self.selfactualSnaleLabel = Label(text="0", size_hint_x=None, width=50)
        actualSnakeLine.add_widget(self.selfactualSnaleLabel)

        self.add_widget(actualSnakeLine)

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


        btn1Line = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        goStartBut = Button(text="Go back", size_hint_x=None, width=100)
        goStartBut.bind(on_press=self.goStartButton)
        btn1Line.add_widget(Label())
        btn1Line.add_widget(goStartBut)
        btn1Line.add_widget(Label())
        self.add_widget(btn1Line)



    def goStartButton(self, instance):
        globalVars.screenManager.current = "Start"

    def generateSnakesButton(self, instance):
        generateThreadHandle = threading.Thread(target=self.generateThread, daemon=True)
        generateThreadHandle.start()

    def generateThread(self):
        self.noOfSnakes = int(self.noOfSnakesTI.text)

        self.generate = True

        for i in range(self.noOfSnakes):
            self.snakes.append(Snake(controlled=False,fieldSize=20))

        counter = 0
        while self.generate:
            for snake in self.snakes:
                while snake.snakeStep(Xdir = 1, Ydir = 0) and snake.noWithoutFood < globalVars.fieldSize * globalVars.fieldSize:
                    pass
                del snake
            self.selfactualSnaleLabel.text = str(counter)
            counter += 1

    def stopSnakeButton(self, instance):
        self.generate = False
