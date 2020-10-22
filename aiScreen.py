import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import globalVars

class AiScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AiScreen, self).__init__(**kwargs)
        
        self.cols = 1

        upGrid = GridLayout(cols=1)
        upGrid.add_widget((Label(text="AiScreen")))
        self.add_widget(upGrid)

        btnLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        goStartBut = Button(text="Go back", size_hint_x=None, width=100)
        goStartBut.bind(on_press=self.goStartButton)
        btnLine.add_widget(Label())
        btnLine.add_widget(goStartBut)
        btnLine.add_widget(Label())
        self.add_widget(btnLine)



    def goStartButton(self, instance):
        globalVars.screenManager.current = "Start"

        if globalVars.buttonPressed.goStartAi == 1:
            globalVars.buttonPressed.goStartAi = 0
        else:
            globalVars.buttonPressed.goStartAi = 1