from math import sin
from random import randint
import time
import sys
import csv

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy_garden.graph import Graph, LinePlot
from kivy.clock import Clock

class graphicsScreen(GridLayout):
    def __init__(self, **kwargs):
        super(graphicsScreen, self).__init__(**kwargs)

        self.dataFile = sys.argv[1]
        self.refreshRate = int(sys.argv[2])

        self.cols = 2
        self.rows = 2


############################ SCORE ##################################################
        self.graphScore = Graph(
            xlabel='Generation',
            ylabel='Score',
            x_ticks_major=1,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            ymin=0,
            xmin=0)

        self.scorePlot = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.scorePlot.points = [(0,0)]
        self.graphScore.add_plot(self.scorePlot)

############################ FITNESS ##################################################
        self.graphFitness = Graph(
            xlabel='Generation',
            ylabel='Fitness',
            x_ticks_major=1,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            ymin=0,
            xmin=0)

        self.fitnessPlot = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.fitnessPlot.points = [(0,0)]
        self.graphFitness.add_plot(self.fitnessPlot)

############################ SCORE TIME ##################################################
        self.graphScoreTime = Graph(
            xlabel='Time [min]',
            ylabel='Score',
            x_ticks_major=1,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            ymin=0,
            xmin=0)

        self.scoreTimePlot = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.scoreTimePlot.points = [(0,0)]
        self.graphScoreTime.add_plot(self.scoreTimePlot)


############################ GENERATION TIME ##################################################
        self.graphGenTime = Graph(
            xlabel='Generation',
            ylabel='Time [min]',
            x_ticks_major=1,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            ymin=0,
            xmin=0)

        self.genTimePlot = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.genTimePlot.points = [(0,0)]
        self.graphGenTime.add_plot(self.genTimePlot)


        
        self.add_widget(self.graphScore)
        self.add_widget(self.graphFitness)
        self.add_widget(self.graphScoreTime)
        self.add_widget(self.graphGenTime)

        if self.refreshRate > 0:
            Clock.schedule_interval(self.readPipeData, self.refreshRate)
        else:
            self.readCsvData()

    def readCsvData(self):
        with open(self.dataFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            score = []
            generation = []
            fitness = []
            seconds = []
            for row in csv_reader:
                if row[0] == 'score':
                    score = list(map(int, row[1][1:-1].split(",")))
                elif row[0] == 'generation':
                    generation = list(map(int, row[1][1:-1].split(",")))
                elif row[0] == 'fitness':
                    fitness = list(map(int, row[1][1:-1].split(",")))
                elif row[0] == 'seconds':
                    seconds = list(map(float, row[1][1:-1].split(",")))

            self.scorePoints = []
            self.fitnessPoints = []
            self.scoreTimePoints = []
            self.timeGenPoints = []
            for i in range(len(score)):
                self.scorePoints.append((generation[i], score[i]))
                self.fitnessPoints.append((generation[i], fitness[i]))
                self.scoreTimePoints.append((seconds[i]/60, score[i]))
                self.timeGenPoints.append((generation[i], seconds[i]/60))

            self.graphsUpdate()


    def readPipeData(self, *args):
        self.scorePoints = []
        self.fitnessPoints = []
        self.scoreTimePoints = []
        self.timeGenPoints = []
        with open(self.dataFile, "r") as file:
            for line in file:
                data = list(line.split(","))
                score = int(data[0])
                generation = int(data[1])
                fitness = int(data[2])
                minutes = float(data[3])/60

                self.scorePoints.append((generation, score))
                self.fitnessPoints.append((generation, fitness))
                self.scoreTimePoints.append((minutes, score))
                self.timeGenPoints.append((generation, minutes))

        self.graphsUpdate()

    def graphsUpdate(self):
        self.scorePlot.points = self.scorePoints
        self.fitnessPlot.points = self.fitnessPoints
        self.scoreTimePlot.points = self.scoreTimePoints
        self.genTimePlot.points = self.timeGenPoints

        xmax = self.scorePlot.points[-1][0]
        self.graphScore.xmax = 10 if xmax < 10 else xmax

        xmax = self.fitnessPlot.points[-1][0]
        self.graphFitness.xmax = 10 if xmax < 10 else xmax

        xmax = round(self.scoreTimePlot.points[-1][0], 1) + 0.1
        self.graphScoreTime.xmax = 1 if xmax < 1 else xmax

        xmax = self.genTimePlot.points[-1][0]
        self.graphGenTime.xmax = 10 if xmax < 10 else xmax
        
        yListScore = []
        for point in self.scorePlot.points:
            yListScore.append(point[1])
        ymax = max(yListScore)
        self.graphScore.ymax = 10 if ymax < 10 else ymax

        yListFitnesse = []
        for point in self.fitnessPlot.points:
            yListFitnesse.append(point[1])
        ymax = max(yListFitnesse)
        self.graphFitness.ymax = 10 if ymax < 10 else ymax

        yListTime = []
        for point in self.scoreTimePlot.points:
            yListTime.append(point[1])
        ymax = max(yListTime)
        self.graphScoreTime.ymax = 10 if ymax < 10 else ymax

        yListGenTime = []
        for point in self.genTimePlot.points:
            yListGenTime.append(point[1])
        ymax = round(max(yListGenTime), 1) + 0.1
        self.graphGenTime.ymax = 1 if ymax < 1 else ymax
        

        self.graphScore.x_ticks_major = int(self.graphScore.xmax/10)
        self.graphFitness.x_ticks_major = int(self.graphFitness.xmax/10)
        self.graphScoreTime.x_ticks_major = float(self.graphScoreTime.xmax/10)
        self.graphGenTime.x_ticks_major = int(self.graphGenTime.xmax/10)

        self.graphScore.y_ticks_major = int(self.graphScore.ymax/10)
        self.graphFitness.y_ticks_major = int(self.graphFitness.ymax/10)
        self.graphScoreTime.y_ticks_major = int(self.graphScoreTime.ymax/10)
        self.graphGenTime.y_ticks_major = float(self.graphGenTime.ymax/10)

class GraphProcess(App):
    def build(self):
        self.icon = 'Icons/snake.png'
        return graphicsScreen()

if __name__ == '__main__':
    GraphProcess().run()


