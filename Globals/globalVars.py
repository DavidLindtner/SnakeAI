from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher

class ButtonPressed(EventDispatcher):
    playButton = NumericProperty(1)
    goStartButton = NumericProperty(1)

def init():
    global screenManager
    global fieldSize
    global fieldSizeSimulate
    global snakeSpeed
    global buttonPressed
    global snakeSpeekSimulate
    global icon

    screenManager = ScreenManager()
    fieldSize = 12
    snakeSpeed = 4
    fieldSizeSimulate = 12
    snakeSpeekSimulate = 4
    buttonPressed = ButtonPressed()
    icon = 'snake.png'



