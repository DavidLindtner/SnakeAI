import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
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
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image  
from kivy.uix.screenmanager import SlideTransition

from Globals import globalVars
from Globals import globalFcns

from snakeBody import Snake


class ImageButton(ButtonBehavior, Image):  
    def on_press(self):
        globalVars.ScreenManager.transition = SlideTransition(direction='right')
        globalVars.screenManager.current = "Start"

        if globalVars.buttonPressed.goStartButton == 1:
            globalVars.buttonPressed.goStartButton = 0
        else:
            globalVars.buttonPressed.goStartButton = 1



Builder.load_string("""  
<ImageButton>:  
    source:'Icons/back.png'  
    size_hint: 0.05, 0.05 
""")  


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
        
############################## FILL PLAY SCREEN ################################################
        field = GridLayout(cols=globalVars.fieldSize, rows=globalVars.fieldSize, row_force_default=False, row_default_height=Window.size[0]/globalVars.fieldSize-1, spacing=1)

        self.screenCell = []

        for i in range(globalVars.fieldSize * globalVars.fieldSize):
            self.screenCell.append(LabelB(bcolor=(0,0,0,1)))
            field.add_widget(self.screenCell[i])

        self.add_widget(field)
        
############################## SPACING ################################################
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

############################## COUNTER LABEL 3 2 1 PLAY ################################################
        self.playBar = Label(text="3", color=(0,1,0,1), font_size='40sp')
        self.add_widget(self.playBar)

        scoreLine = GridLayout(cols=7, rows=1, row_force_default=True, row_default_height=40)

        self.scoreLabel = Label(text='1', font_size='20sp', size_hint_x=None, width=50)
        self.movesLabel = Label(text='0', font_size='20sp', size_hint_x=None, width=50)

############################## SCORE MOVES ################################################
        scoreLine.add_widget(Label())
        scoreLine.add_widget(Label(text='Score:', font_size='20sp', size_hint_x=None, width=100))
        scoreLine.add_widget(self.scoreLabel)
        scoreLine.add_widget(Label())
        scoreLine.add_widget(Label(text='Moves:', font_size='20sp', size_hint_x=None, width=100))
        scoreLine.add_widget(self.movesLabel)
        scoreLine.add_widget(Label())

        self.add_widget(scoreLine)

############################## LABELS INFO ################################################
        foodLine = GridLayout(cols=7, rows=1, row_force_default=True, row_default_height=60)
        self.movesWithoutFoodLabel = Label(text='0', font_size='18sp', size_hint_x=None, width=50)
        self.foodMovesRatioLabel = Label(text='0', font_size='18sp', size_hint_x=None, width=50)

        foodLine.add_widget(Label())
        foodLine.add_widget(Label(text='      Moves \nwithout food:', font_size='18sp', size_hint_x=None, width=100))
        foodLine.add_widget(self.movesWithoutFoodLabel)
        foodLine.add_widget(Label())
        foodLine.add_widget(Label(text='Moves to\nfood ratio:', font_size='18sp', size_hint_x=None, width=100))
        foodLine.add_widget(self.foodMovesRatioLabel)
        foodLine.add_widget(Label())

        self.add_widget(foodLine)

############################## BUTTONS ################################################
        botLine = BoxLayout(orientation='horizontal', spacing=10)
        playAgainBut = Button(text="Play again", size_hint=(0.4, 0.6))
        playAgainBut.bind(on_press=self.playAgainButton)
        botLine.add_widget(Label(text='', size_hint=(0.05, 0.6)))
        botLine.add_widget(ImageButton(size_hint=(.1, 0.6)))
        botLine.add_widget(Label(text='', size_hint=(0.1, 0.6)))
        botLine.add_widget(playAgainBut)
        botLine.add_widget(Label(text='', size_hint=(0.25, 0.6)))
        self.add_widget(botLine)

        self.add_widget(Label())

        self.snake = Snake()

        self.newGame()

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
        if self.snake.snakeStep(Xdir = self.moveX, Ydir = self.moveY):
            self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field)
        else:
            if self.snake.win:
                self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field)
                self.event.cancel()
                self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field, opacity=0.5)
                self.moveX = 0
                self.moveY = 0
                self.playBar.text = "YOU WIN"
                self.playBar.font_size='20sp'
            else:
                self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field)
                self.event.cancel()
                self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field, opacity=0.5)
                self.moveX = 0
                self.moveY = 0
                self.playBar.text = "GAME OVER"
                self.playBar.font_size='20sp'

        self.scoreLabel.text = str(self.snake.score)
        self.movesLabel.text = str(self.snake.noOfMoves)
        self.movesWithoutFoodLabel.text = str(self.snake.noWithoutFood)
        self.foodMovesRatioLabel.text = str(round(self.snake.foodMovesRatio,1))


    def playAgainButton(self, instance):
        self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field, opacity=0.5)
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
        del self.snake
        self.moveX = 0
        self.moveY = 0
        self.snake = Snake(intelligence=False)
        self.drawScreen(0)

    def newGameCount3(self, instance):
        self.event = Clock.schedule_interval(self.drawScreen, 1/globalVars.snakeSpeed)
        self.playBar.text = "PLAY"
        self.playBar.font_size='20sp'
