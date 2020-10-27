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

        Window.size = (400, 400)

        self.fieldSize = int(sys.argv[1])+2
        self.snakeSpeed = float(sys.argv[2])
        self.fileName = sys.argv[3]
        self.indexWeight = int(sys.argv[4])

        self.readWeightCsv(self.fileName)

        self.cols = 1

        self.field = GridLayout(cols=self.fieldSize, rows=self.fieldSize, row_force_default=False, row_default_height=Window.size[0]/self.fieldSize-1, spacing=1)

        self.screenCell = []

        for i in range(self.fieldSize * self.fieldSize):
            self.screenCell.append(LabelB(bcolor=(0,0,0,1)))
            self.field.add_widget(self.screenCell[i])

        self.add_widget(self.field)

        self.event = Clock.schedule_interval(self.drawScreen, 1/self.snakeSpeed)

        self.snake = Snake(intelligence=True,fieldSize=self.fieldSize-2)
        self.snake.importBrain(self.weights[self.indexWeight])


    def drawScreen(self, instance):
        if self.snake.snakeStep():
            #print("fitness")
            #print(self.snake.fitness)
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
                if row[0] == 'weights':
                    self.weights.append(list(map(float, row[1][1:-1].split(','))))


class SimulateSnake(App):
    def build(self):
        return SimulateScreen()


if __name__ == '__main__':
    SimulateSnake().run()