
class Selection():
    def __init__(self):
        pass

    def selectBestRank(self, fitness, percentage):
        fitnessList = fitness
        numOut = int(len(fitnessList) * percentage)
        outList = []
        for i in range(numOut):
            maxIndex = fitnessList.index(max(fitnessList))
            fitnessList[maxIndex] = 0
            outList.append(maxIndex)

        return outList


        


