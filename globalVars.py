from kivy.uix.screenmanager import ScreenManager, Screen

def init():
    global screenManager
    global fieldSize
    global snakeSpeed

    screenManager = ScreenManager()
    fieldSize = 12
    snakeSpeed = 4
