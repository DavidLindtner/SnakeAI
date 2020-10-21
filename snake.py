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


kivy.require("1.11.1")

globalVars.init()


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
        


        btnLine = GridLayout(cols=3, row_force_default=True, row_default_height=40)

        self.play = Button(text="PLAY", size_hint_x=None, width=150)
        btnLine.add_widget(Label(text=""))
        btnLine.add_widget(self.play)
        btnLine.add_widget(Label(text=""))
        self.play.bind(on_press=self.playButton)

        self.add_widget(btnLine)



    def playButton(self, instance):

        globalVars.fieldSize = int(self.fieldSizeTI.text) + 2
        globalVars.snakeSpeed = float(self.snakeSpeedTI.text)

        snakeApp.createPlayScreen()
        snakeApp.screenManager.current = "Play"



Builder.load_string("""
<LabelB>:
    bcolor: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

""")

class LabelB(Label):
    bcolor = ListProperty([1,1,1,1])


class PlayScreen(GridLayout):

    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)

        self.moveX = 0
        self.moveY = 0

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.cols = 1

        self.field = GridLayout(cols=globalVars.fieldSize, rows=globalVars.fieldSize, row_force_default=False, row_default_height=Window.size[0]/globalVars.fieldSize, spacing=1)

        self.screenCell = []

        for i in range(globalVars.fieldSize * globalVars.fieldSize):
            self.screenCell.append(LabelB(bcolor=(0,0,0,1)))
            self.field.add_widget(self.screenCell[i])

        self.add_widget(self.field)

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

        self.playBar = Label(text="3", color=(0,1,0,1), font_size='40sp')
        self.add_widget(self.playBar)

        self.snake = Snake(controlled=True)
        self.newGame()

        scoreLine = GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40)
        self.scoreLabel = Label(text='1', font_size='20sp', size_hint_x=None, width=30)
        scoreLine.add_widget(Label(text='SCORE:', font_size='20sp', size_hint_x=None, width=100))
        scoreLine.add_widget(self.scoreLabel)
        scoreLine.add_widget(Label())

        self.add_widget(scoreLine)


        btnLine = GridLayout(cols=5, rows=2, row_force_default=True, row_default_height=40)

        self.playAgainBut = Button(text="Play again", size_hint_x=None, width=100)
        self.goStartBut = Button(text="Go back", size_hint_x=None, width=100)
        btnLine.add_widget(Label(text=""))
        btnLine.add_widget(self.playAgainBut)
        btnLine.add_widget(Label(text=""))
        btnLine.add_widget(self.goStartBut)
        btnLine.add_widget(Label(text=""))
        self.playAgainBut.bind(on_press=self.playAgainButton)
        self.goStartBut.bind(on_press=self.goStartButton)

        self.add_widget(btnLine)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'right':
            self.moveX = 1
            self.moveY = 0
        elif keycode[1] == 'left':
            self.moveX = -1
            self.moveY = 0
        elif keycode[1] == 'down':
            self.moveX = 0
            self.moveY = 1
        elif keycode[1] == 'up':
            self.moveX = 0
            self.moveY = -1
        return True


    def drawScreen(self, instance):
        self.scoreLabel.text = str(self.snake.score)
        if self.snake.snakeStep(Xdir = self.moveX, Ydir = self.moveY):
            self.drawField(field=self.snake.field)
        else:
            self.drawField(field=self.snake.field)
            self.event.cancel()
            self.drawField(field=self.snake.field, opacity=0.5)
            self.moveX = 0
            self.moveY = 0
            self.playBar.text = "GAME OVER"
            self.playBar.font_size='20sp'


    def drawField(self, field, opacity=1):
        i = 0
        for cell in self.screenCell:
            if field[i] == 0:
                cell.bcolor=(0,0,0,opacity)                
            elif field[i] == 1:
                cell.bcolor=(1,1,1,opacity)  
            elif field[i] == 2:
                cell.bcolor=(1,1,1,opacity)  
            elif field[i] == 3:
                cell.bcolor=(0,1,0,opacity)  
            elif field[i] == 4:
                cell.bcolor=(0.2,0.2,0.2,opacity)
            elif field[i] == 5:
                cell.bcolor=(1,0,0,opacity)
            else:
                cell.bcolor=(0,0,0,opacity)
            i = i + 1

    def playAgainButton(self, instance):
        self.drawField(field=self.snake.field, opacity=0.5)
        try:
            self.event.cancel()
            self.event1.cancel()
            self.event2.cancel()
            self.event3.cancel()
        except:
            pass

        self.moveX = 0
        self.moveY = 0
        self.newGame()

    def goStartButton(self, instance):
        try:
            self.event.cancel()
        except:
            pass
        snakeApp.screenManager.current = "Start"
        snakeApp.destroyPlayScreen()


    def newGame(self):
        self.playBar.text = "3"
        self.playBar.font_size='40sp'
        self.event1 = Clock.schedule_once(self.newGameCount1, 1)

    def newGameCount1(self, instance):
        self.playBar.text = "2"
        self.playBar.font_size='40sp'
        self.event2 = Clock.schedule_once(self.newGameCount2, 1)

    def newGameCount2(self, instance):
        self.playBar.text = "1"
        self.playBar.font_size='40sp'
        self.event3 = Clock.schedule_once(self.newGameCount3, 1)

    def newGameCount3(self, instance):
        del self.snake
        self.moveX = 1
        self.moveY = 0
        self.snake = Snake(controlled=True)
        self.event = Clock.schedule_interval(self.drawScreen, 1/globalVars.snakeSpeed)
        self.playBar.text = "PLAY"
        self.playBar.font_size='20sp'

class SnakeAI(App):

    def build(self):
        self.screenManager = ScreenManager()

        self.startScreen = StartScreen()
        self.screen = Screen(name="Start")
        self.screen.add_widget(self.startScreen)
        self.screenManager.add_widget(self.screen)

        Window.size = (350, 600)

        return self.screenManager

    def createPlayScreen(self):
        self.playScreen = PlayScreen()
        self.screen = Screen(name="Play")
        self.screen.add_widget(self.playScreen)
        self.screenManager.add_widget(self.screen)

    def destroyPlayScreen(self):
        del self.playScreen
        self.screenManager.remove_widget(self.screen)


if __name__ == '__main__':

    snakeApp = SnakeAI()
    snakeApp.run()

    
    


