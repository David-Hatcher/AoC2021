'''Global Defs'''
INPUTREAL = 'input.txt'
INPUTTEST = 'inputtest.txt'

def getIncreaseCount(inputs):
    arr = inputs[:]
    increaseCount = 0
    lastCount = arr.pop(0)
    while arr:
        if (currentCount := arr.pop(0)) > lastCount:
            increaseCount += 1
        lastCount = currentCount
    return increaseCount

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    inputs = []
    for line in lines:
        inputs.append(int(line.strip()))
    return inputs

def getIncreaseCountSliding(inputs):
    lastThree = inputs[:3]
    arr = inputs[3:]
    increaseCount = 0
    while arr:
        currentValue = lastThree.pop(0)
        nextValue = arr.pop(0)
        lastThree.append(nextValue)
        if nextValue > currentValue:
            increaseCount += 1
    return increaseCount


'''Main'''
inputs = getInputs(INPUTREAL)

'''Part One'''
increaseCount = getIncreaseCount(inputs)
print(increaseCount)

'''Part Two'''
increaseCount = getIncreaseCountSliding(inputs)
print(increaseCount)