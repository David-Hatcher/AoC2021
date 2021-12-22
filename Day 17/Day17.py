from math import sqrt, floor
'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'
GRAV = 1
DRAG = 1

def getInputs(fileName):
    file = open(fileName,'r')
    line = file.readline()
    file.close()
    line = line.split(', ')
    y = line[1].split('=')[1].split('..')
    yUpper = int(y[1])
    yLower = int(y[0])
    x = line[0].split(' ')[2].split('=')[1].split('..')
    xLower = int(x[0])
    xUpper = int(x[1])
    return xLower, xUpper, yLower, yUpper


def getSummation(number):
    return int((number * (number + 1))/2)

def invertSummation(number,returnNeg = False):
    nOne = (-1 + sqrt(1 + (8*number))/2)
    nTwo = (-1 - sqrt(1 + (8*number))/2)
    if nOne > 0 and not returnNeg:
        return nOne
    return nTwo

def isProjectileInBounds(x,y,bounds):
    if bounds['left'] <= x <= bounds['right'] and bounds['bottom'] <= y <= bounds['top']:
        return True
    return False

def getMaxVelocities(bounds):
    return bounds['right'], floor(invertSummation(bounds['left'])), bounds['bottom'], -bounds['bottom']

def getReasonableVelocities(xMin,xMax,yMin,yMax):
    velocities = []
    for x in range(xMin,xMax + 1):
        for y in range(yMin, yMax + 1):
            velocities.append([x,y])
    return velocities

def getGoodVelocitiesCount(bounds,initialVelocities):
    goodVelocities = []

    for v in initialVelocities:
        currentV = v
        currentPosition = [0,0]
        while currentPosition[0] <= bounds['right'] and currentPosition[1] >= bounds['bottom']:
            currentPosition[0] += currentV[0]
            currentPosition[1] += currentV[1]
            if currentV[0] > 0:
                currentV[0] -= DRAG
            if currentV[0] < 0:
                currentV[0] += DRAG
            currentV[1] -= GRAV
            if isProjectileInBounds(currentPosition[0],currentPosition[1],bounds):
                goodVelocities.append(v)
                break
    return len(goodVelocities)

boundsPackage = getInputs(INPUTREAL)

bounds = {
    'left' : boundsPackage[0],
    'right' : boundsPackage[1],
    'bottom' : boundsPackage[2],
    'top' : boundsPackage[3]
}

'''Part One'''
yHigh = getSummation(bounds['bottom'])
print(yHigh)

'''Part Two'''
vXMax, vXMin, vYMin, vYMax = getMaxVelocities(bounds)
initialVelocities = getReasonableVelocities(vXMin, vXMax, vYMin, vYMax)
goodVelocitiesCount = getGoodVelocitiesCount(bounds,initialVelocities)
print(goodVelocitiesCount)
