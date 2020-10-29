from random import randint
from kivy.core.window import Window

from Globals import globalVars
from Intelligence.brain import Brain

#   COLORS
#   Background  0   black
#   Snake       1   white
#   Head        6   yellow
#   Eat         3   green
#   Border      4   grey
#   Crash       5   red

class Snake():
    def __init__(self, intelligence=False, fieldSize=0):
        self.intelligence = intelligence
        fs = fieldSize
        if fs == 0:
            self.fieldSize = globalVars.fieldSize
        else:
            self.fieldSize = fieldSize + 2

        self.field = [0] * self.fieldSize * self.fieldSize

        #if self.fieldSize % 2 == 0:
        #    self.parts = [int(self.fieldSize*self.fieldSize/2 - self.fieldSize/2 - 1)]
        #else:
        #    self.parts = [int(self.fieldSize*self.fieldSize/2 - 1)]

        self.last = 0
        self.moveX = 0
        self.moveY = 0
        self.score = 1
        self.noOfMoves = 0
        self.noWithoutFood = 0
        self.foodMovesRatio = 1
        self.fitness = 0
        self.win = False

#   E, NE, N, NW, W, SW, S, SE
        self.distWall = [0] * 8
        self.seeWall = [0] * 8
        self.seeFood = [0] * 8
        self.seeSnake = [0] * 8
        self.distSnake = [0] * 8
        self.distFood = [0] * 8
        self.lastMove = [0] * 4
        self.see = []

        self.setBorder()
        self.generateEat()
        self.parts = [self.findRandAvailablePlace()]


    def randomBrain(self, noOfNeuron1, noOfNeuron2):
        self.brain = Brain(noOfNeuron1=noOfNeuron1, noOfNeuron2=noOfNeuron2)

    def importBrain(self, rates, noOfNeuron1, noOfNeuron2):
        self.brain = Brain(noOfNeuron1=noOfNeuron1, noOfNeuron2=noOfNeuron2)
        self.brain.importWeight(rates)

    def exportBrain(self):
        return self.brain.exportWeight()

    def exportDimBrain(self):
        return [self.brain.noOfInputs, self.brain.noOfNeuron1Layer, self.brain.noOfNeuron2Layer]

    def setBorder(self):
        self.field[0:self.fieldSize] = [4] * self.fieldSize
        for i in range(self.fieldSize):
            self.field[i*self.fieldSize-1] = 4
            self.field[i*self.fieldSize] = 4
        self.field[self.fieldSize * self.fieldSize-self.fieldSize:self.fieldSize * self.fieldSize-1] = [4] * self.fieldSize


    def snakeStep(self, Xdir=0, Ydir=0):
        if Xdir != 0 or Ydir != 0:
            self.moveX = Xdir
            self.moveY = Ydir

        self.last = self.parts[-1]

        if self.win:
            self.calculateFitness()
            return False

        
        self.snakeMove()
        self.calculateFitness()
        #self.countVision()

        #   hit snake
        if self.field[self.parts[0]] == 1:
            self.calculateFitness()
            self.field[self.parts[1]] = 1
            self.field[self.parts[0]] = 5
            self.moveX = 0
            self.moveY = 0
            return False

        #   hit border
        if self.field[self.parts[0]] == 4:
            self.calculateFitness()
            self.field[self.parts[0]] = 5
            if len(self.parts) >= 2:
                self.field[self.parts[1]] = 1
            self.moveX = 0
            self.moveY = 0
            return False

        #   hit food
        if self.field[self.parts[0]] == 3:
            self.eat()

        self.field[self.parts[0]] = 6
        if len(self.parts) >= 2:
            self.field[self.parts[1]] = 1

        return True


    def snakeMove(self):
        if self.intelligence:
            self.countVision()
            self.brain.think(input=self.see)
            if self.brain.outputList[0] == 1:
                self.moveX = 1
                self.moveY = 0
            elif self.brain.outputList[1] == 1:
                self.moveX = 0
                self.moveY = 1
            elif self.brain.outputList[2] == 1:
                self.moveX = -1
                self.moveY = 0
            elif self.brain.outputList[3] == 1:
                self.moveX = 0
                self.moveY = -1

        if self.moveX == 1 and self.moveY == 0:
            self.parts.insert(0, self.parts[0]+1)
            self.field[self.parts[-1]] = 0
            self.parts.pop()
        elif self.moveX == -1 and self.moveY == 0:
            self.parts.insert(0, self.parts[0]-1)
            self.field[self.parts[-1]] = 0
            self.parts.pop()
        elif self.moveX == 0 and self.moveY == 1:
            self.parts.insert(0, self.parts[0]+self.fieldSize)
            self.field[self.parts[-1]] = 0
            self.parts.pop()
        elif self.moveX == 0 and self.moveY == -1:
            self.parts.insert(0, self.parts[0]-self.fieldSize)
            self.field[self.parts[-1]] = 0
            self.parts.pop()

        if self.moveX != 0 or self.moveY != 0:
            self.noWithoutFood += 1
            self.noOfMoves += 1
            self.foodMovesRatio = self.noOfMoves / self.score

    def eat(self):
        self.score += 1
        self.noWithoutFood = 0

        self.parts.insert(len(self.parts), self.last)
        self.field[self.parts[-1]] = 1

        self.generateEat()

    def generateEat(self):
        randPos = self.findRandAvailablePlace()
        if randPos == 0:
            self.win = True
        else:
            self.field[randPos] = 3

    def findRandAvailablePlace(self):
        counter = 0
        availablePlaces = []
        for cell in self.field:
            if cell == 0:
                availablePlaces.append(counter)
            counter += 1

        if availablePlaces:
            randPos = availablePlaces[randint(0, len(availablePlaces)-1)]
        else:
            randPos = 0

        return randPos


    def calculateFitness(self):
        self.fitness = self.score*self.score*self.score*self.score + self.noOfMoves

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

            self.distWall[i] = counter-1

            position = self.parts[0]
            counter = 0

        self.seeWall = [0] * 8
        for i in range(8):
            if self.distWall[i] == 0:
                self.seeWall[i] = 10
                
        self.reverseDistWall = [0] * 8
        for i in range(8):
            self.reverseDistWall[i] = self.fieldSize - self.distWall[i]


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

            self.distFood[i] = counter-1

            position = self.parts[0]
            counter = 0
            
        for i in range(8):
            if self.distFood[i] != self.distWall[i]:
                self.seeFood[i] = 10
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

            self.distSnake[i] = counter-1

            position = self.parts[0]
            counter = 0
            
        for i in range(8):
            if self.distSnake[i] != self.distWall[i]:
                self.seeSnake[i] = 10
            else:
                self.seeSnake[i] = 0

        self.lastMove = [0] * 4

        if self.moveX == 1 and self.moveY == 0:
            self.lastMove[0] = 1
        elif self.moveX == 0 and self.moveY == 1:
            self.lastMove[1] = 1
        elif self.moveX == -1 and self.moveY == 0:
            self.lastMove[2] = 1
        elif self.moveX == 0 and self.moveY == -1:
            self.lastMove[3] = 1

        self.see = self.seeWall + self.seeSnake + self.seeFood #+ self.lastMove

        #print(" ")
        #print("distWall : " + str(self.distWall))
        #print("seeWall  : " + str(self.seeWall))
        #print("seeFood  : " + str(self.seeFood))
        #print("seeSnake : " + str(self.seeSnake))
        #print("distSnake: " + str(self.distSnake))
        #print("distFood : " + str(self.distFood))
