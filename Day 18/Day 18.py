from math import floor, ceil
import copy
'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'
IS = 'inputsample.txt'



def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    file.close()
    inputs = []
    for line in lines:
        inputs.append(line.strip())
    return inputs

def findExplode(str):
    openCount = 0
    for i in range(len(str)):
        if str[i] == '[':
            openCount += 1
        elif str[i] == ']':
            openCount -= 1
        if openCount == 5:
            return i
    return i

def getBracketToSplit(str,firstExplode):
    explodeBracket = str.index(']',firstExplode)
    return explodeBracket + 1

def getBracket(str,start,finish):
    bracket = [int(x) for x in str[start:finish].replace(']','').replace('[','').split(',')]
    return bracket

def findNextNumber(str,rightBracket):
    firstIndex,secondIndex = 0,0
    for i in range(rightBracket,len(str)):
        if str[i] not in [']','[',','] and firstIndex == 0:
            firstIndex = i
        elif str[i] in [']','[',','] and firstIndex != 0:
            secondIndex = i
            break
    return firstIndex, secondIndex

def findPreviousNumber(str,leftBracket):
    firstIndex, secondIndex = 0,0
    for i in range(leftBracket,0,-1):
        if str[i] not in [']','[',','] and firstIndex == 0:
            firstIndex = i
        elif str[i] in [']','[',','] and firstIndex != 0:
            secondIndex = i
            break
    if firstIndex == 0 and secondIndex == 0:
        return 0, 0
    else:
        return firstIndex + 1, secondIndex + 1

def explode(string):
    if (firstBracket := findExplode(string)) < len(string) - 1:
        secondBracket = getBracketToSplit(string,firstBracket)
        explodeBracket = getBracket(string,firstBracket,secondBracket)
        nextNumberStart, nextNumberEnd = findNextNumber(string,secondBracket)
        prevNumberEnd, prevNumberStart = findPreviousNumber(string,firstBracket)
        prevNumberToReplace, nextNumberToReplace = False, False
        previousNumber, nextNumber = 0,0
        if prevNumberEnd != 0 and prevNumberStart != 0:
            previousNumber = int(string[prevNumberStart:prevNumberEnd])
            prevNumberToReplace = True
        if nextNumberStart != 0 and nextNumberEnd != 0:
            nextNumber = int(string[nextNumberStart:nextNumberEnd])
            nextNumberToReplace = True
        if prevNumberToReplace and nextNumberToReplace:
            explodedString = string[:prevNumberStart] + str(explodeBracket[0] + previousNumber) + string[prevNumberEnd:firstBracket] + str(0) +  string[secondBracket:nextNumberStart] + str(explodeBracket[1] + nextNumber) + string[nextNumberEnd:] 
        elif not prevNumberToReplace and nextNumberToReplace:
            explodedString = string[:firstBracket] + str(0) +  string[secondBracket:nextNumberStart] + str(explodeBracket[1] + nextNumber) + string[nextNumberEnd:] 
        elif prevNumberToReplace and not nextNumberToReplace:
            explodedString = string[:prevNumberStart] + str(explodeBracket[0] + previousNumber) + string[prevNumberEnd:firstBracket] + str(0) +  string[secondBracket:]
        elif not prevNumberToReplace and not nextNumberToReplace:
            explodedString = string[:firstBracket] + str(0) +  string[secondBracket:]
        return True, explodedString
    return False, string

def findNumberToSplit(string):
    lastNonNumber = 0
    for i in range(len(string)):
        if string[i] in ['[',',',']']:
            lastNonNumber = i
        if i - lastNonNumber >= 2:
            return lastNonNumber + 1, i + 1
    return 0,0

def splitValue(string):
    if (splitBounds := findNumberToSplit(string)) != (0,0):
        splitNumber = int(string[splitBounds[0]: splitBounds[1]])
        splitString = string[:splitBounds[0]] + f'[{floor(splitNumber/2)},{ceil(splitNumber/2)}]' + string[splitBounds[1]:]
        return True, splitString
    return False, string

def reduceSnailNumbers(string):
    reducedString = string
    while True:
        hasSplit, hasExplode = False, False
        hasExplode, reducedString = explode(reducedString)
        if hasExplode:
            continue
        hasSplit, reducedString = splitValue(reducedString)
        if hasSplit:
            continue
        if hasSplit == False and hasExplode == False:
            break
    return reducedString

def addSnailNumber(firstNumber, secondNumber):
    return f'[{firstNumber},{secondNumber}]'

def doesStringContainPair(string):
    for i in range(len(string) - 4):
        if string[i] == '[' and string[i+4] == ']':
            return True, i, i+4
    else:
        return False, 0, 0

def findPair(string):
    firstBracket = 0
    for i in range(len(string)):
        if string[i] == '[':
            firstBracket = i
        elif string[i] == ']':
            return True, firstBracket, i
    return False, 0, 0

def getMagnitude(snailNumber):
    finalSnailNumber = snailNumber
    while True:
        needMoreAddition, start, end = findPair(finalSnailNumber)
        if needMoreAddition:
            numbers = [int(x) for x in finalSnailNumber[start:end + 1].replace(']','').replace('[','').split(',')]
            replaceNumber = 3*numbers[0] + 2*numbers[1]
            finalSnailNumber = finalSnailNumber[:start] + str(replaceNumber) + finalSnailNumber[end + 1:]
        else: 
            break
    return finalSnailNumber

def getFinalSnailNumber(inputs):
    fullSnailNumber = ''
    for i in range(len(inputs)):
        if i == 0:
            fullSnailNumber = reduceSnailNumbers(inputs[i])
        else:
            currentSnailNumber = reduceSnailNumbers(inputs[i])
            fullSnailNumber = addSnailNumber(fullSnailNumber,currentSnailNumber)
            fullSnailNumber = reduceSnailNumbers(fullSnailNumber)
    return fullSnailNumber

def getMaxMagnitude(inputs):
    maxMagnitude = 0
    for inputA in inputs:
        for inputB in inputs:
            if inputA != inputB:
                reducedA = reduceSnailNumbers(inputA)
                reducedB = reduceSnailNumbers(inputB)
                addedAB = addSnailNumber(reducedA, reducedB)
                addedBA = addSnailNumber(reducedB, reducedA)
                reducedAB = reduceSnailNumbers(addedAB)
                reducedBA = reduceSnailNumbers(addedBA)
                magAB = int(getMagnitude(reducedAB))
                magBA = int(getMagnitude(reducedBA))
                if magAB > maxMagnitude:
                    maxMagnitude = magAB
                if magBA > maxMagnitude:
                    maxMagnitude = magBA
    return maxMagnitude

inputs = getInputs(INPUTREAL)

'''Part One'''
fullSnailNumber = getFinalSnailNumber(inputs)
print('Magnitude',getMagnitude(fullSnailNumber))


'''Part Two'''
maxMagnitude = getMaxMagnitude(inputs)
print('Max Magnitude',maxMagnitude)