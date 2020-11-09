from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.lang import Builder
import csv
import sys

from Globals import globalFcns
from Globals import globalVars

from snakeBody import Snake



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

class SimulateScreen(GridLayout):

    def __init__(self, **kwargs):
        super(SimulateScreen, self).__init__(**kwargs)

        Window.size = (400, 600)

        self.fieldSize = int(sys.argv[1])+2
        self.snakeSpeed = float(sys.argv[2])
        self.fileName = sys.argv[3]
        self.indexWeight = int(sys.argv[4])

        self.readWeightCsv(self.fileName)

        self.cols = 1

########################### SIMULATION FIELD #############################################################
        field = GridLayout(cols=self.fieldSize, rows=self.fieldSize, row_force_default=False, row_default_height=Window.size[0]/self.fieldSize-1, spacing=1)

        self.screenCell = []

        for i in range(self.fieldSize * self.fieldSize):
            self.screenCell.append(LabelB(bcolor=(0,0,0,1)))
            field.add_widget(self.screenCell[i])

        self.add_widget(field)

########################### SIMULATE AGAIN BUTTON #############################################################
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

        againLine = GridLayout(cols=3, row_force_default=True, row_default_height=40)
        againBut = Button(text='Again', size_hint_x=None, width=150)
        againBut.bind(on_press=self.againButton)
        againLine.add_widget(Label())
        againLine.add_widget(againBut)
        againLine.add_widget(Label())
        self.add_widget(againLine)

############################## SCORE MOVES ################################################
        scoreLine = GridLayout(cols=7, rows=1, row_force_default=True, row_default_height=40)

        self.scoreLabel = Label(text='1', size_hint_x=None, width=50)
        self.movesLabel = Label(text='0', size_hint_x=None, width=50)

        scoreLine.add_widget(Label())
        scoreLine.add_widget(Label(text='Score:', size_hint_x=None, width=100))
        scoreLine.add_widget(self.scoreLabel)
        scoreLine.add_widget(Label())
        scoreLine.add_widget(Label(text='Moves:', size_hint_x=None, width=100))
        scoreLine.add_widget(self.movesLabel)
        scoreLine.add_widget(Label())

        self.add_widget(scoreLine)

############################## LABELS INFO ################################################
        foodLine = GridLayout(cols=7, rows=1, row_force_default=True, row_default_height=60)
        self.movesWithoutFoodLabel = Label(text='0', size_hint_x=None, width=50)
        self.foodMovesRatioLabel = Label(text='0', size_hint_x=None, width=50)

        foodLine.add_widget(Label())
        foodLine.add_widget(Label(text='      Moves \nwithout food:', size_hint_x=None, width=100))
        foodLine.add_widget(self.movesWithoutFoodLabel)
        foodLine.add_widget(Label())
        foodLine.add_widget(Label(text='Moves to\nfood ratio:', size_hint_x=None, width=100))
        foodLine.add_widget(self.foodMovesRatioLabel)
        foodLine.add_widget(Label())

        self.add_widget(foodLine)


        

        self.snake = Snake(intelligence=True,fieldSize=self.fieldSize-2)
        self.snake.importBrain(rates=self.weights[self.indexWeight].copy(),  noOfNeuron1=self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)

        self.event = Clock.schedule_interval(self.drawScreen, 1/self.snakeSpeed)


    def againButton(self, instance):
        self.event.cancel()
        del self.snake

        self.snake = Snake(intelligence=True,fieldSize=self.fieldSize-2)
        self.snake.importBrain(rates=self.weights[self.indexWeight].copy(),  noOfNeuron1=self.noOfNeuron1Layer, noOfNeuron2=self.noOfNeuron2Layer)

        self.event = Clock.schedule_interval(self.drawScreen, 1/self.snakeSpeed)

    def drawScreen(self, instance):
        self.scoreLabel.text = str(self.snake.score)
        self.movesLabel.text = str(self.snake.noOfMoves)
        self.movesWithoutFoodLabel.text = str(self.snake.noWithoutFood)
        self.foodMovesRatioLabel.text = str(round(self.snake.foodMovesRatio,1))

        if self.snake.snakeStep():
            self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field)
        else:
            if self.snake.win:
                self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field)
                self.event.cancel()
                self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field, opacity=0.5)
            else:
                self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field)
                self.event.cancel()
                self.screenCell = globalFcns.drawField(screenCell=self.screenCell, field=self.snake.field, opacity=0.5)


    def readWeightCsv(self, fileName):
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.weights = []
            for row in csv_reader:
                if row[0] == 'noOfNeuron1Layer':
                    self.noOfNeuron1Layer = int(row[1])
                if row[0] == 'noOfNeuron2Layer':
                    self.noOfNeuron2Layer = int(row[1])
                if row[0] == 'weights':
                    self.weights.append(list(map(float, row[1][1:-1].split(','))))


class SimulateSnake(App):
    def build(self):
        self.icon = 'Icons/snake.png'
        return SimulateScreen()


if __name__ == '__main__':
    SimulateSnake().run()