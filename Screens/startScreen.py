import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.clock import Clock
#from kivy.core.window import Window

from Globals import globalVars

    
class StartScreen(GridLayout):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        self.cols = 1
        self.add_widget(Label(text='SNAKE AI', font_size='30sp'))

        dimLine = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        dimLine.add_widget(Label(text='FIELD DIMENSIONS', size_hint_x=None, width=300, font_size='20sp'))

        self.fieldSizeTI = TextInput(multiline=False, text=str(globalVars.fieldSize-2), size_hint_x=None, width=50, font_size='20sp')
        dimLine.add_widget(self.fieldSizeTI)

        self.add_widget(dimLine)

        spdLine = GridLayout(cols=3, row_force_default=True, row_default_height=40)

        spdLine.add_widget(Label(text='SPEED', size_hint_x=None, width=200, font_size='20sp'))
        self.snakeSpeedTI = TextInput(multiline=False, text=str(globalVars.snakeSpeed), size_hint_x=None, width=50, font_size='20sp')
        spdLine.add_widget(self.snakeSpeedTI)
        spdLine.add_widget(Label(text='cell/s', size_hint_x=None, width=100, font_size='20sp'))

        self.add_widget(spdLine)
        


        btn1Line = GridLayout(cols=3, row_force_default=True, row_default_height=50)

        self.play = Button(text="Play", size_hint_x=None, width=200, font_size='20sp')
        btn1Line.add_widget(Label(text=""))
        btn1Line.add_widget(self.play)
        btn1Line.add_widget(Label(text=""))
        self.play.bind(on_press=self.playButton)

        self.add_widget(btn1Line)


        btn2Line = GridLayout(cols=5, row_force_default=True, row_default_height=50)

        self.aiConf = Button(text="Setup AI", size_hint_x=None, width=200, font_size='20sp')
        self.aiResult = Button(text="See results", size_hint_x=None, width=200, font_size='20sp')
        btn2Line.add_widget(Label())
        btn2Line.add_widget(self.aiConf)
        btn2Line.add_widget(Label())
        btn2Line.add_widget(self.aiResult)
        btn2Line.add_widget(Label())
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

        globalVars.ScreenManager.transition = SlideTransition(direction='down')
        globalVars.screenManager.current = "Play"

    def aiConfButton(self, instance):
        globalVars.fieldSize = int(self.fieldSizeTI.text) + 2
        globalVars.snakeSpeed = float(self.snakeSpeedTI.text)

        globalVars.ScreenManager.transition = SlideTransition(direction='right')
        globalVars.screenManager.current = "AiConf"

    def aiResButton(self, instance):
        globalVars.fieldSize = int(self.fieldSizeTI.text) + 2
        globalVars.snakeSpeed = float(self.snakeSpeedTI.text)

        globalVars.ScreenManager.transition = SlideTransition(direction='left')
        globalVars.screenManager.current = "AiRes"
