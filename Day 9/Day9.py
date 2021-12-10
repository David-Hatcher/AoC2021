import numpy as np
'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    inputs = []
    for line in lines:
        numList = list(line.strip())
        numList = list(map(int,numList))
        inputs.append(numList)     
    file.close()   
    return inputs

def getRowsCols(inputs):
    return len(inputs), len(inputs[0])

def isThisLowPoint(heights,i,j,rows,cols):
    currentNumber = heights[i][j]
    if j - 1 >= 0:
        leftNum = heights[i][j - 1]
        if leftNum <= currentNumber:
            return False
    if j + 1 <= cols - 1:
        rightNum = heights[i][j + 1]
        if rightNum <= currentNumber:
            return False
    if i - 1 >= 0:
        topNum = heights[i - 1][j]
        if topNum <= currentNumber:
            return False
    if i + 1 <= rows - 1:
        downNum = heights[i + 1][j]
        if downNum <= currentNumber:
            return False
    return True

def getLowPoints(heights,rows,cols):
    riskPoints = []
    for i in range(rows):
        for j in range(cols):
            if isThisLowPoint(heights,i,j,rows,cols):
                riskPoints.append(heights[i][j] + 1)
    return riskPoints

def createCheckedMap(heights,rows,cols):
    checkedMap = []
    for i in range(rows):
        checkedMap.append([])
        for j in range(cols):
            checkedMap[i].append([heights[i][j],'unchecked'])
    return checkedMap

def findBasins(heights,rows,cols):
    basinSizes = []
    for i in range(rows):
        for j in range(cols):
            if heights[i][j][0] != 9 and heights[i][j][1] != 'checked':
                basinSizes.append(findBasin(heights,i,j,rows,cols))
    return basinSizes

def findBasin(heights,i,j,rows,cols):
    #check current value and add one to the basin size
    heights[i][j][1] = 'checked'
    basinSize = 1
    #base case, current points out of bounds, don't recurse
    if i < 0 or i > rows or j < 0 or j > cols:
        pass
    #check up
    if i - 1 >= 0 and heights[i-1][j][0] != 9 and heights[i-1][j][1] != 'checked':
        basinSize += findBasin(heights,i-1,j,rows,cols)
    #check down
    if i + 1 <= rows -1 and heights[i+1][j][0] != 9 and heights[i+1][j][1] != 'checked':
        basinSize += findBasin(heights,i+1,j,rows,cols)
    #check left
    if j - 1 >= 0 and heights[i][j-1][0] != 9 and heights[i][j-1][1] != 'checked':
        basinSize += findBasin(heights,i,j-1,rows,cols)
    #check right
    if j + 1 <= cols - 1 and heights[i][j+1][0] != 9 and heights[i][j+1][1] != 'checked':
        basinSize += findBasin(heights,i,j+1,rows,cols)
    return basinSize


inputs = getInputs(INPUTREAL)
rows, cols = getRowsCols(inputs)

'''Part One'''
riskPoints = getLowPoints(inputs,rows,cols)
riskPointSum = sum(riskPoints)
print(riskPointSum)

'''Part Two'''
checkedMap = createCheckedMap(inputs,rows,cols)
basinSizes = findBasins(checkedMap,rows,cols)
basinSizesSorted = sorted(basinSizes,reverse=True)
basinSizesTopThreeSum = basinSizesSorted[0] * basinSizesSorted[1] * basinSizesSorted[2]
print(basinSizesTopThreeSum)