import numpy as np

'''Global Defs'''
INPUTREAL = 'input.txt'
INPUTTEST = 'inputtest.txt'

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    
    xOne,yOne,xTwo,yTwo = [],[],[],[]
    for line in lines:
        firstSplit = line.split(' -> ')
        posOne = firstSplit[0].split(',')
        posTwo = firstSplit[1].split(',')
        xOne.append(int(posOne[0]))
        yOne.append(int(posOne[1]))
        xTwo.append(int(posTwo[0]))
        yTwo.append(int(posTwo[1]))
    file.close()
    return xOne, yOne, xTwo, yTwo

def findMaxValues(x,y,xx,yy):
    yMax = max(max(y),max(yy))
    xMax = max(max(x),max(xx))
    return xMax, yMax

def addPath(diagram,x1,y1,x2,y2,partTwo = False):
    arr = diagram.view()
    if x1 == x2:
        rangeVal = abs(y2-y1)
        negMove = y2 - y1 < 0
        for i in range(rangeVal + 1):
            addValue = -i if negMove else i
            arr[y1 + addValue,x1] += 1
    elif y1 == y2:
        rangeVal = abs(x2-x1)
        negMove = x2 - x1 < 0
        for i in range(rangeVal + 1):
            addValue = -i if negMove else i
            arr[y1,x1 + addValue] += 1
    else:
        if partTwo == True:
            rangeVal = abs(x2-x1)
            negMoveX = x2 - x1 < 0
            negMoveY = y2 - y1 < 0
            for i in range(rangeVal + 1):
                addValY = -i if negMoveY else i
                addValX = -i if negMoveX else i
                arr[y1 + addValY,x1 + addValX] += 1
    return arr

def countOverlaps(diagram):
    bounds = np.shape(diagram)
    overlapCount = 0
    for i in range(bounds[0]):
        for j in range(bounds[1]):
            if diagram[i][j] > 1:
                overlapCount += 1
    return overlapCount

def printDiagram(diagram):
    arr = diagram.astype(int).astype(str).view()
    arr[arr == '0'] = '.'
    print(arr)


x1, y1, x2, y2 = getInputs(INPUTREAL)
xMax, yMax = findMaxValues(x1,y1,x2,y2)

'''Part One'''
diagram = np.zeros((xMax + 1,yMax + 1))
for x,y,xx,yy in zip(x1, y1, x2, y2):
    # print(f'{x},{y} -> {xx},{yy}')
    diagram = addPath(diagram,x,y,xx,yy)
    # printDiagram(diagram)

overlaps = countOverlaps(diagram)
print(overlaps)


'''Part Two'''
diagram = np.zeros((xMax + 1,yMax + 1))

for x,y,xx,yy in zip(x1, y1, x2, y2):
    # print(f'{x},{y} -> {xx},{yy}')
    diagram = addPath(diagram,x,y,xx,yy,True)
    # printDiagram(diagram)

overlaps = countOverlaps(diagram)
print(overlaps)
# printDiagram(diagram)