import numpy as np
'''Global Defs'''
INPUTREAL = 'input.txt'
INPUTTEST = 'inputtest.txt'

def getInputs(fileName):
    file = open(fileName,'r')
    line = [int(x) for x in file.readline().strip().split(',')]
    file.close()   
    return line

def findBestLine(crabs):
    bestFuel = float('inf')
    numbersTried = []
    for i in range(max(crabs)):
        currentNumberTest = i
        numbersTried.append(currentNumberTest)
        currentFuel = 0
        for j in range(len(crabs)):
            currentFuel += abs(crabs[j] - i)
            if currentFuel > bestFuel:
                break
        if currentFuel < bestFuel:
            bestFuel = currentFuel
    return bestFuel
    pass

def findBestLineSum(crabs):
    bestFuel = float('inf')
    numbersTried = []
    for i in range(max(crabs)):
        currentFuel = 0
        for j in range(len(crabs)):
            n = abs(crabs[j] - i)
            currentFuel += int((n**2 + n)/2)
            if currentFuel > bestFuel:
                break
        if currentFuel < bestFuel:
            bestFuel = currentFuel
    return bestFuel

crabs = getInputs(INPUTREAL)
# print(crabs)

bestFuel = findBestLine(crabs)
print(bestFuel)

bestFuelSum = findBestLineSum(crabs)
print(bestFuelSum)