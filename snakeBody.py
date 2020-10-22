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
    def __init__(self,controlled=True,fieldSize=0):

        if fieldSize == 0:
            self.fieldSize = globalVars.fieldSize
        else:
            self.fieldSize = fieldSize + 2

        self.field = [0] * self.fieldSize * self.fieldSize
        self.parts = [int(self.fieldSize+1), int(self.fieldSize+1)]
        self.moveX = 0
        self.moveY = 0
        self.score = 1
        self.noOfMoves = 0
        self.noWithoutFood = 0
        self.foodMovesRatio = 1

#   E, NE, N, NW, W, SW, S, SE
        self.distWall = [0] * 8
        self.seeFood = [0] * 8
        self.seeSnake = [0] * 8
        self.distSnake = [0] * 8
        self.distFood = [0] * 8

        self.setBorder()
        self.generateEat()
    

    def setBorder(self):
        self.field[0:self.fieldSize] = [4] * self.fieldSize
        for i in range(self.fieldSize):
            self.field[i*self.fieldSize-1] = 4
            self.field[i*self.fieldSize] = 4
        self.field[self.fieldSize * self.fieldSize-self.fieldSize:self.fieldSize * self.fieldSize-1] = [4] * self.fieldSize


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

        self.countVision()

        return True


    def snakeMove(self):
        if self.moveX == 1 and self.moveY == 0:
            self.parts.insert(0, self.parts[0]+1)
            self.parts.pop()
        elif self.moveX == -1 and self.moveY == 0:
            self.parts.insert(0, self.parts[0]-1)
            self.parts.pop()
        elif self.moveX == 0 and self.moveY == 1:
            self.parts.insert(0, self.parts[0]+self.fieldSize)
            self.parts.pop()
        elif self.moveX == 0 and self.moveY == -1:
            self.parts.insert(0, self.parts[0]-self.fieldSize)
            self.parts.pop()

        self.noWithoutFood += 1
        self.noOfMoves += 1
        self.foodMovesRatio = self.noOfMoves / self.score

    def eat(self):
        self.score += 1
        self.noWithoutFood = 0

        self.parts.append(self.parts[-1])
        self.field[self.parts[-1]] = 1
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

    def countVision(self):
        #   BORDER
        position = self.parts[0]
        counter = 0

        for i in range(8):
            while self.field[position] != 4:
                if i == 0:
                    position = position + 1
                    counter += 1
                elif i == 1:
                    position = position - self.fieldSize + 1
                    counter += 1
                elif i == 2:
                    position = position - self.fieldSize
                    counter += 1
                elif i == 3:
                    position = position - self.fieldSize - 1
                    counter += 1
                elif i == 4:
                    position = position - 1
                    counter += 1
                elif i == 5:
                    position = position + self.fieldSize - 1
                    counter += 1
                elif i == 6:
                    position = position + self.fieldSize
                    counter += 1
                else:
                    position = position + self.fieldSize + 1
                    counter += 1

            self.distWall[i] = counter

            position = self.parts[0]
            counter = 0

        self.distFood = [0] * 8
        #   SEE FOOD
        for i in range(8):
            while self.field[position] != 3 and self.field[position] != 4:
                if i == 0:
                    position = position + 1
                    counter += 1
                elif i == 1:
                    position = position - self.fieldSize + 1
                    counter += 1
                elif i == 2:
                    position = position - self.fieldSize
                    counter += 1
                elif i == 3:
                    position = position - self.fieldSize - 1
                    counter += 1
                elif i == 4:
                    position = position - 1
                    counter += 1
                elif i == 5:
                    position = position + self.fieldSize - 1
                    counter += 1
                elif i == 6:
                    position = position + self.fieldSize
                    counter += 1
                else:
                    position = position + self.fieldSize + 1
                    counter += 1

            self.distFood[i] = counter

            position = self.parts[0]
            counter = 0
            
        for i in range(8):
            if self.distFood[i] != self.distWall[i]:
                self.seeFood[i] = 1
            else:
                self.seeFood[i] = 0
                self.distFood[i] = self.fieldSize


        #   SEE SNAKE
        for i in range(8):
            while self.field[position] != 1 and self.field[position] != 4:
                if i == 0:
                    position = position + 1
                    counter += 1
                elif i == 1:
                    position = position - self.fieldSize + 1
                    counter += 1
                elif i == 2:
                    position = position - self.fieldSize
                    counter += 1
                elif i == 3:
                    position = position - self.fieldSize - 1
                    counter += 1
                elif i == 4:
                    position = position - 1
                    counter += 1
                elif i == 5:
                    position = position + self.fieldSize - 1
                    counter += 1
                elif i == 6:
                    position = position + self.fieldSize
                    counter += 1
                else:
                    position = position + self.fieldSize + 1
                    counter += 1

            self.distSnake[i] = counter

            position = self.parts[0]
            counter = 0
            
        for i in range(8):
            if self.distSnake[i] != self.distWall[i]:
                self.seeSnake[i] = 1
            else:
                self.seeSnake[i] = 0
