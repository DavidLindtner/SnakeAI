import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window

import globalVars



class StartScreen(GridLayout):

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        self.cols = 1
        self.add_widget(Label(text='SNAKE AI'))

        dimLine = GridLayout(cols=2, row_force_default=True, row_default_height=30)
        dimLine.add_widget(Label(text='FIELD DIMENSIONS', size_hint_x=None, width=200))

        self.fieldSizeTI = TextInput(multiline=False, text=str(globalVars.fieldSize-2), size_hint_x=None, width=50)
        dimLine.add_widget(self.fieldSizeTI)

        self.add_widget(dimLine)


        spdLine = GridLayout(cols=3, row_force_default=True, row_default_height=30)

        spdLine.add_widget(Label(text='SPEED', size_hint_x=None, width=150))
        self.snakeSpeedTI = TextInput(multiline=False, text=str(globalVars.snakeSpeed), size_hint_x=None, width=50)
        spdLine.add_widget(self.snakeSpeedTI)
        spdLine.add_widget(Label(text='cell/s', size_hint_x=None, width=50))

        self.add_widget(spdLine)
        


        btn1Line = GridLayout(cols=3, row_force_default=True, row_default_height=40)

        self.play = Button(text="Play", size_hint_x=None, width=150)
        btn1Line.add_widget(Label(text=""))
        btn1Line.add_widget(self.play)
        btn1Line.add_widget(Label(text=""))
        self.play.bind(on_press=self.playButton)

        self.add_widget(btn1Line)


        btn2Line = GridLayout(cols=5, row_force_default=True, row_default_height=40)

        self.aiConf = Button(text="Setup AI", size_hint_x=None, width=150)
        self.aiResult = Button(text="See results", size_hint_x=None, width=150)
        btn2Line.add_widget(Label(text=""))
        btn2Line.add_widget(self.aiConf)
        btn2Line.add_widget(Label(text=""))
        btn2Line.add_widget(self.aiResult)
        btn2Line.add_widget(Label(text=""))
        self.aiConf.bind(on_press=self.aiConfButton)
        self.aiResult.bind(on_press=self.aiResButton)

        self.add_widget(btn2Line)



    def playButton(self, instance):

        globalVars.fieldSize = int(self.fieldSizeTI.text) + 2
        globalVars.snakeSpeed = float(self.snakeSpeedTI.text)

        if globalVars.buttonPressed.playButton == 1:
            globalVars.buttonPressed.playButton = 0
        else:
            globalVars.buttonPressed.playButton = 1

        globalVars.screenManager.current = "Play"

    def aiConfButton(self, instance):
        globalVars.fieldSize = int(self.fieldSizeTI.text) + 2
        globalVars.snakeSpeed = float(self.snakeSpeedTI.text)

        globalVars.screenManager.current = "AiConf"

    def aiResButton(self, instance):
        globalVars.fieldSize = int(self.fieldSizeTI.text) + 2
        globalVars.snakeSpeed = float(self.snakeSpeedTI.text)

        globalVars.screenManager.current = "AiRes"
