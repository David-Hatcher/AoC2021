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
    s = 0
    for key, value in digitCount.items():
        s += value
    return s

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
                if (set.union(keys[1],keys[4],keys[7]).issubset(p)):
                    keys[9] = p
                elif set.union(keys[1],keys[7]).issubset(p) and not keys[4].issubset(p):
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
    # print(input)
    firstHalf,secondHalf = inputs.split('|')
    patterns, values = firstHalf.split(), secondHalf.split()
    keys = {}
    getEasyNumbers(keys,patterns)

    getHardNumbers(keys,patterns)

    s = ''
    for value in values:
        value = set(value)
        for k,v in keys.items():
            if v == value:
                s += str(k)
    return s


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
