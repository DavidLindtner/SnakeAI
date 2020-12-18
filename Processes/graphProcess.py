import multiprocessing

from math import sin
from random import randint
import time
import sys
import csv
import os
import os
if os.name == 'nt':
	import ctypes
	ctypes.windll.shcore.SetProcessDpiAwareness(1)


import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy_garden.graph import Graph, LinePlot
from kivy.clock import Clock

from kivy.core.window import Window

class GraphProcess(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        global dataFile
        global refreshRate
        dataFile, refreshRate = self.task_queue.get()
        GraphView().run()


class graphicsScreen(GridLayout):
    def __init__(self, **kwargs):
        super(graphicsScreen, self).__init__(**kwargs)

        global dataFile
        self.dataFile = dataFile
        global refreshRate
        self.refreshRate = refreshRate
        Window.size = (800, 600)
        self.cols = 2
        self.rows = 2


############################ SCORE ##################################################
        self.graphScore = Graph(
            xlabel='Generation',
            ylabel='Score',
            font_size='20sp',
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
        self.scorePlotMedian = LinePlot(color=[0.3, 0.3, 1, 1], line_width=2)
        self.scorePlot.points = [(0,0)]
        self.scorePlotMedian.points = [(0,0)]
        self.graphScore.add_plot(self.scorePlot)
        self.graphScore.add_plot(self.scorePlotMedian)

############################ FITNESS ##################################################
        self.graphFitness = Graph(
            xlabel='Generation',
            ylabel='Fitness',
            font_size='20sp',
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
        self.fitnessPlotMedian = LinePlot(color=[0.3, 0.3, 1, 1], line_width=2)
        self.fitnessPlot.points = [(0,0)]
        self.fitnessPlotMedian.points = [(0,0)]
        self.graphFitness.add_plot(self.fitnessPlot)
        self.graphFitness.add_plot(self.fitnessPlotMedian)

############################ SCORE TIME ##################################################
        self.graphScoreTime = Graph(
            xlabel='Time [min]',
            ylabel='Score',
            font_size='20sp',
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
        self.scoreTimePlotMedian = LinePlot(color=[0.3, 0.3, 1, 1], line_width=2)
        self.scoreTimePlot.points = [(0,0)]
        self.scoreTimePlotMedian.points = [(0,0)]
        self.graphScoreTime.add_plot(self.scoreTimePlot)
        self.graphScoreTime.add_plot(self.scoreTimePlotMedian)


############################ GENERATION TIME ##################################################
        self.graphGenTime = Graph(
            xlabel='Generation',
            ylabel='Time [min]',
            font_size='20sp',
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
            self.readHandle = Clock.schedule_interval(self.readPipeData, self.refreshRate)
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
            self.scorePointsMedian = []
            self.fitnessPoints = []
            self.fitnessPointsMedian = []
            self.scoreTimePoints = []
            self.scoreTimePointsMedian = []
            self.timeGenPoints = []
            for i in range(len(score)):
                self.scorePoints.append((generation[i], score[i]))
                self.fitnessPoints.append((generation[i], fitness[i]))
                self.scoreTimePoints.append((seconds[i]/60, score[i]))
                self.timeGenPoints.append((generation[i], seconds[i]/60))

            self.scorePointsMedian = self.floatMedian(self.scorePoints)
            self.fitnessPointsMedian = self.floatMedian(self.fitnessPoints)
            self.scoreTimePointsMedian = self.floatMedian(self.scoreTimePoints)
            self.graphsUpdate()


    def readPipeData(self, *args):
        self.scorePoints = []
        self.scorePointsMedian = []
        self.fitnessPoints = []
        self.fitnessPointsMedian = []
        self.scoreTimePoints = []
        self.scoreTimePointsMedian = []
        self.timeGenPoints = []
        if os.path.exists(self.dataFile):
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

            self.scorePointsMedian = self.floatMedian(self.scorePoints)
            self.fitnessPointsMedian = self.floatMedian(self.fitnessPoints)
            self.scoreTimePointsMedian = self.floatMedian(self.scoreTimePoints)
            self.graphsUpdate()
        else:
            self.readHandle.cancel()


    def graphsUpdate(self):
        self.scorePlot.points = self.scorePoints
        self.scorePlotMedian.points = self.scorePointsMedian

        self.fitnessPlot.points = self.fitnessPoints
        self.fitnessPlotMedian.points = self.fitnessPointsMedian

        self.scoreTimePlot.points = self.scoreTimePoints
        self.scoreTimePlotMedian.points = self.scoreTimePointsMedian

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
        ymax = round(max(yListGenTime), 1)
        self.graphGenTime.ymax = 1 if ymax < 1 else ymax
        

        self.graphScore.x_ticks_major = int(self.graphScore.xmax/10)
        self.graphFitness.x_ticks_major = int(self.graphFitness.xmax/10)
        self.graphScoreTime.x_ticks_major = float(self.graphScoreTime.xmax/10)
        self.graphGenTime.x_ticks_major = int(self.graphGenTime.xmax/10)

        self.graphScore.y_ticks_major = int(self.graphScore.ymax/10)
        self.graphFitness.y_ticks_major = int(self.graphFitness.ymax/10)
        self.graphScoreTime.y_ticks_major = int(self.graphScoreTime.ymax/10)
        self.graphGenTime.y_ticks_major = float(self.graphGenTime.ymax/10)

    def floatMedian(self, points):
        retPoints = []
        if len(points) > 4:
            tmpPoints = [0] * len(points)

            for i in range(len(points)):
                tmpPoints[i] = points[i][1]

            for i in range(4):
                retPoints.append((points[i][0], points[i][1]))

            for i in range(len(points)-9-4):
                retPoints.append((points[i+4][0], sorted(tmpPoints[i+4:i+4+9])[4]))

        return retPoints

class GraphView(App):
    def build(self):
        self.icon = 'Icons/snake.png'
        return graphicsScreen()


