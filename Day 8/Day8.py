import numpy as np
'''Global Defs'''
INPUTREAL = 'input.txt'
INPUTTEST = 'inputtest.txt'

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    inputs = []
    for line in lines:
        line = line.strip()
        inputs.append(line)
    file.close()   
    return inputs

def getOutputDigits(inputs):
    digits = []
    for value in inputs:
        digitList = value.split(' | ')[1]
        digitList = digitList.split(' ')
        digits.append(digitList)
    return digits

def convertToNumber(digit):
    if len(digit) == 2:
        return 1
    elif len(digit) == 4:
        return 4
    elif len(digit) == 3:
        return 7
    elif len(digit) == 7:
        return 8
    else:
        return None

def getOutputDigitCount(outputDigits):
    digitCount = {i:0 for i in range(10)}
    for digits in outputDigits:
        for digit in digits:
            # print(digit)
            number = convertToNumber(digit)
            # print(number)
            if number != None:
                digitCount[number] += 1
    return digitCount


def digitSum(digitCount):
    sumDigits = 0
    for key, value in digitCount.items():
        sumDigits += value
    return sumDigits

def getEasyNumbers(keys,patterns):
    for p in patterns:
        length = len(p)
        p = set(p)
        if length == 2:
            keys[1] = p
        elif length == 3:
            keys[7] = p
        elif length == 4:
            keys[4] = p
        elif length == 7:
            keys[8] = p

def getHardNumbers(keys,patterns):
        for p in patterns:
            length = len(p)
            p = set(p)
            if length == 6:
                if (set.union(keys[4],keys[7]).issubset(p)):
                    keys[9] = p
                elif keys[1].issubset(p) and not keys[4].issubset(p):
                    keys[0] = p
                else:
                    keys[6] = p
            elif length == 5:
                if keys[1].issubset(p):
                    keys[3] = p
                elif (keys[4] - keys[1]).issubset(p):
                    keys[5] = p
                else:
                    keys[2] = p

def getNumbers(inputs):
    firstHalf,secondHalf = inputs.split('|')
    patterns, outputs = firstHalf.split(), secondHalf.split()
    keys = {}
    getEasyNumbers(keys,patterns)
    getHardNumbers(keys,patterns)
    numberString = ''
    keysFlipped = {''.join(sorted(list(value))):key for key,value in keys.items()}
    for output in outputs:
        output = ''.join(sorted(list(output)))
        if output in keysFlipped:
            numberString += str(keysFlipped[output])
    return numberString


inputs = getInputs(INPUTREAL)
oDigits = getOutputDigits(inputs)
oDigitCounts = getOutputDigitCount(oDigits)

'''Part One'''
count = digitSum(oDigitCounts)
print(count)

'''Part Two'''
inputs = getInputs(INPUTREAL)
outputCount = 0
for input in inputs:
    outputCount += int(getNumbers(input))

print(outputCount)
