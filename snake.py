import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.factory import Factory
from kivy.lang import Builder

import globalVars
from startScreen import StartScreen
from playScreen import PlayScreen
from aiScreen import AiScreen
from aiResultsScreen import AiResultScreen

kivy.require("1.11.1")

globalVars.init()


class SnakeAI(App):

    def build(self):
        self.icon = 'snake.png'

        globalVars.buttonPressed.bind(playButton=self.createPlayScreen)
        globalVars.buttonPressed.bind(goStartButton=self.destroyPlayScreen)

        self.startScreen = StartScreen()
        self.screen = Screen(name="Start")
        self.screen.add_widget(self.startScreen)
        globalVars.screenManager.add_widget(self.screen)

        self.aiScreen = AiScreen()
        self.screenAi = Screen(name="AiConf")
        self.screenAi.add_widget(self.aiScreen)
        globalVars.screenManager.add_widget(self.screenAi)

        self.aiScreenRes = AiResultScreen()
        self.screenAiRes = Screen(name="AiRes")
        self.screenAiRes.add_widget(self.aiScreenRes)
        globalVars.screenManager.add_widget(self.screenAiRes)

        Window.size = (350, 600)

        return globalVars.screenManager

    def createPlayScreen(self, instance, value):
        self.playScreen = PlayScreen()
        self.screenPlay = Screen(name="Play")
        self.screenPlay.add_widget(self.playScreen)
        globalVars.screenManager.add_widget(self.screenPlay)

    def destroyPlayScreen(self, instance, value):
        del self.playScreen
        globalVars.screenManager.remove_widget(self.screenPlay)

if __name__ == '__main__':

    snakeApp = SnakeAI()
    snakeApp.run()

    
    


