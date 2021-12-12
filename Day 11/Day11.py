'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'



def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    octopi = []
    for line in lines:
        row = [[int(x),'unflashed'] for x in line.strip()]
        octopi.append(row)
    file.close()
    return octopi

def printOcto(octo):
    for row in octo:
        row = [str(x[0]) for x in row]
        print(''.join(row))

def anOctoNeedsToFlash(octoMatrix):
    for octoRow in octoMatrix:
        for octo in octoRow:
            if octo[1] == 'unflashed' and octo[0] >= 9:
                return True
    return False

def performStep(octoMatrix):
    pass

def increaseOctoEnergy(octoMatrix):
    for octoRow in octoMatrix:
        for octo in octoRow:
            octo[0] += 1

def flashOctoRecursive(octoMatrix,i,j,rows,cols):
    if octoMatrix[i][j][0] > 9 and octoMatrix[i][j][1] != 'flashed':
        # print(i,j)
        # octoMatrix[i][j][0] = 0
        octoMatrix[i][j][1] = 'flashed'
        flashed = 1
        if i - 1 >= 0:
            octoMatrix[i-1][j][0] += 1
            flashed += flashOctoRecursive(octoMatrix,i-1,j,rows,cols)
        if i + 1 <= rows - 1:
            octoMatrix[i+1][j][0] += 1
            flashed += flashOctoRecursive(octoMatrix,i+1,j,rows,cols)
        if j - 1 >= 0:
            octoMatrix[i][j-1][0] += 1
            flashed += flashOctoRecursive(octoMatrix,i,j-1,rows,cols)
        if j + 1 <= cols - 1:
            octoMatrix[i][j+1][0] += 1
            flashed += flashOctoRecursive(octoMatrix,i,j+1,rows,cols)
        if j + 1 <= cols - 1 and i + 1 <= rows - 1:
            octoMatrix[i+1][j+1][0] += 1
            flashed += flashOctoRecursive(octoMatrix,i+1,j+1,rows,cols)
        if j - 1 >= 0 and i - 1 >= 0:
            octoMatrix[i-1][j-1][0] += 1
            flashed += flashOctoRecursive(octoMatrix,i-1,j-1,rows,cols)
        if j - 1 >= 0 and i + 1 <= rows - 1:
            octoMatrix[i+1][j-1][0] += 1
            flashed += flashOctoRecursive(octoMatrix,i+1,j-1,rows,cols)
        if j + 1 <= cols - 1 and i - 1 >= 0:
            octoMatrix[i-1][j+1][0] += 1
            flashed += flashOctoRecursive(octoMatrix,i-1,j+1,rows,cols)
        return flashed
    else:
        return 0

def zeroFlashedOcto(octoMatrix):
    for octoRow in octoMatrix:
        for octo in octoRow:
            if octo[1] == 'flashed':
                octo[0] = 0

def resetFlashedOcto(octoMatrix):
    for octoRow in octoMatrix:
        for octo in octoRow:
            octo[1] = 'unflashed'

def doSteps(octoMatrix,stepCount,rows,cols):
    flashCount = 0
    for _ in range(stepCount):
        increaseOctoEnergy(octoMatrix)
        for i in range(len(octoMatrix)):
            for j in range(len(octoMatrix[i])):
                if octoMatrix[i][j][0] > 9 and octoMatrix[i][j][1] != 'flashed':
                    flashCount += flashOctoRecursive(octoMatrix,i,j,rows,cols)
        zeroFlashedOcto(octoMatrix)
        resetFlashedOcto(octoMatrix)
    return flashCount

def findFirstFullFlash(octoMatrix,rows,cols):
    stepCount = 0
    while True:
        stepCount += 1
        flashCount = 0
        increaseOctoEnergy(octoMatrix)
        for i in range(len(octoMatrix)):
            for j in range(len(octoMatrix)):
                if octoMatrix[i][j][0] > 9 and octoMatrix[i][j][1] != 'flashed':
                    flashCount = flashOctoRecursive(octoMatrix,i,j,rows,cols)
        if flashCount == rows * cols:
            return stepCount
        else:
            zeroFlashedOcto(octoMatrix)
            resetFlashedOcto(octoMatrix)


octopi = getInputs(INPUTREAL)
rows = len(octopi)
cols = len(octopi[0])

'''Part One'''
flashedCount = doSteps(octopi,100,rows,cols)
print(flashedCount)


'''Part Two'''
octopi = getInputs(INPUTREAL)
fullFlashStep = findFirstFullFlash(octopi,rows,cols)
print(fullFlashStep)