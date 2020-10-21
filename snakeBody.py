from random import randint
from kivy.core.window import Window

import globalVars

#   COLORS
#   Background  0   black
#   Snake       1   white
#   Eat         3   green
#   Border      4   grey
#   Crash       5   red

class Snake():
    def __init__(self,controlled=True):

        self.field = [0] * globalVars.fieldSize * globalVars.fieldSize
        self.parts = [int(globalVars.fieldSize+1), int(globalVars.fieldSize+1)]
        self.moveX = 0
        self.moveY = 0
        self.score = 1

        self.setBorder()
        self.generateEat()
    

    def setBorder(self):
        self.field[0:globalVars.fieldSize] = [4] * globalVars.fieldSize
        for i in range(globalVars.fieldSize):
            self.field[i*globalVars.fieldSize-1] = 4
            self.field[i*globalVars.fieldSize] = 4
        self.field[globalVars.fieldSize * globalVars.fieldSize-globalVars.fieldSize:globalVars.fieldSize * globalVars.fieldSize-1] = [4] * globalVars.fieldSize


    def snakeStep(self, Xdir, Ydir):
        self.moveX = Xdir
        self.moveY = Ydir

        self.snakeMove()

        #   hit food
        if self.field[self.parts[0]] == 3:
            self.eat()

        #   hit snake
        if self.field[self.parts[0]] == 1:
            self.field[self.parts[-1]] = 0
            self.field[self.parts[0]] = 5
            self.stopMove()
            return False

        #   hit border
        if self.field[self.parts[0]] == 4:
            self.field[self.parts[-1]] = 0
            self.field[self.parts[0]] = 5
            self.stopMove()
            return False

        self.field[self.parts[-1]] = 0
        self.field[self.parts[0]] = 1

        return True


    def snakeMove(self):
        if self.moveX == 1 and self.moveY == 0:
            self.parts.insert(0, self.parts[0]+1)
            self.parts.pop()
        elif self.moveX == -1 and self.moveY == 0:
            self.parts.insert(0, self.parts[0]-1)
            self.parts.pop()
        elif self.moveX == 0 and self.moveY == 1:
            self.parts.insert(0, self.parts[0]+globalVars.fieldSize)
            self.parts.pop()
        elif self.moveX == 0 and self.moveY == -1:
            self.parts.insert(0, self.parts[0]-globalVars.fieldSize)
            self.parts.pop()


    def eat(self):
        self.score += 1
        self.parts.append(self.parts[-1])
        self.generateEat()

    def generateEat(self):
        foodPos = 0
        counter = 0

        availablePlaces = []
        for cell in self.field:
            if cell == 0:
                availablePlaces.append(counter)
            counter += 1

        if availablePlaces:
            foodPos = availablePlaces[randint(0, len(availablePlaces)-1)]

        self.field[foodPos] = 3

    def stopMove(self):
        self.moveX = 0
        self.moveY = 0




