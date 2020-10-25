    
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