import numpy as np

def drawField(screenCell, field, opacity=1):
    i = 0
    for cell in screenCell:
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
        elif field[i] == 6:
            cell.bcolor=(1,1,0.5,opacity)
        else:
            cell.bcolor=(0,0,0,opacity)
        i = i + 1
        
    return screenCell


def net2list(w1, w2, w3, b1, b2, b3):
    w1Sh = w1.shape
    w2Sh = w2.shape
    w3Sh = w3.shape

    b1Sh = b1.shape
    b2Sh = b2.shape
    b3Sh = b3.shape

    rates = []
    for i in range(w1Sh[0]):
        for j in range(w1Sh[1]):
            rates.append(w1[i,j])

    for i in range(b1Sh[0]):
        rates.append(b1[i,0])

    for i in range(w2Sh[0]):
        for j in range(w2Sh[1]):
            rates.append(w2[i,j])

    for i in range(b2Sh[0]):
        rates.append(b2[i,0])

    for i in range(w3Sh[0]):
        for j in range(w3Sh[1]):
            rates.append(w3[i,j])

    for i in range(b3Sh[0]):
        rates.append(b3[i,0])

    return rates

def list2net(w1Sh, w2Sh, w3Sh, b1Sh, b2Sh, b3Sh, rates):
    w1 = np.zeros(w1Sh)
    for i in range(w1Sh[0]):
        w1[i:i+1] = rates[0:w1Sh[1]]
        for j in range(w1Sh[1]):
            rates.pop(0)

    b1 = np.zeros(b1Sh)
    for i in range(b1Sh[0]):
        b1[i] = rates[0]
        rates.pop(0)

    w2 = np.zeros(w2Sh)
    for i in range(w2Sh[0]):
        w2[i:i+1] = rates[0:w2Sh[1]]
        for j in range(w2Sh[1]):
            rates.pop(0)

    b2 = np.zeros(b2Sh)
    for i in range(b2Sh[0]):
        b2[i] = rates[0]
        rates.pop(0)

    w3 = np.zeros(w3Sh)
    for i in range(w3Sh[0]):
        w3[i:i+1] = rates[0:w3Sh[1]]
        for j in range(w3Sh[1]):
            rates.pop(0)

    b3 = np.zeros(b3Sh)
    for i in range(b3Sh[0]):
        b3[i] = rates[0]
        rates.pop(0)

    return [w1, w2, w3, b1, b2, b3]