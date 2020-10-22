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
from snakeBody import Snake
from aiScreen import AiScreen
from startScreen import StartScreen
from playScreen import PlayScreen

kivy.require("1.11.1")

globalVars.init()


class SnakeAI(App):

    def build(self):
        self.icon = 'snake.png'

        globalVars.buttonPressed.bind(playButton=self.createPlayScreen)
        globalVars.buttonPressed.bind(goStartButton=self.destroyPlayScreen)
        globalVars.buttonPressed.bind(aiButton=self.createAiScreen)
        globalVars.buttonPressed.bind(goStartAi=self.destroyAiScreen)

        self.startScreen = StartScreen()
        self.screen = Screen(name="Start")
        self.screen.add_widget(self.startScreen)
        globalVars.screenManager.add_widget(self.screen)

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


    def createAiScreen(self, instance, value):
        self.aiScreen = AiScreen()
        self.screenAi = Screen(name="Ai")
        self.screenAi.add_widget(self.aiScreen)
        globalVars.screenManager.add_widget(self.screenAi)

    def destroyAiScreen(self, instance, value):
        del self.aiScreen
        globalVars.screenManager.remove_widget(self.screenAi)


if __name__ == '__main__':

    snakeApp = SnakeAI()
    snakeApp.run()

    
    


