from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher

class ButtonPressed(EventDispatcher):
    playButton = NumericProperty(1)
    goStartButton = NumericProperty(1)
    aiButton = NumericProperty(1)
    goStartAi = NumericProperty(1)

def init():
    global screenManager
    global fieldSize
    global snakeSpeed
    global buttonPressed

    screenManager = ScreenManager()
    fieldSize = 12
    snakeSpeed = 4
    buttonPressed = ButtonPressed()



