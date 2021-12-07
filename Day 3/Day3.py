'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    inputs = []
    for line in lines:
        inputs.append(line.strip())
    return inputs

def getMostCommonBits(inputs):
    n = len(inputs[0])
    ithBits = [[] for _ in range(n)]
    mostCommonBits = ''
    for bits in inputs:
        for i in range(len(bits)):
            ithBits[i].append(bits[i])
    for bits in ithBits:
        countOnes = bits.count('1')
        mostCommonBits += '1' if countOnes > len(bits)/2 else '0'
    return mostCommonBits

def getGammaEpsilon(commonBits):
    gamma = int(commonBits,2)
    epsilon = int(''.join('1' if x == '0' else '0' for x in commonBits),2)
    return gamma*epsilon

def getCommonBitsCurrent(bitsList,i,most):
    if len(bitsList) == 1:
        return bitsList[0]
    onesCount,zerosCount = 0,0
    zeros, ones = [], []
    for bits in bitsList:
        if bits[i] == '1':
            onesCount += 1
            ones.append(bits)
        elif bits[i] == '0':
            zeros.append(bits)
            zerosCount += 1
    if (most and zerosCount > onesCount) or (not most and zerosCount <= onesCount):
            return getCommonBitsCurrent(zeros,i+1,most)
    else: 
            return getCommonBitsCurrent(ones,i+1,most)

def getLifeSupportRating(ogr,csr):
    return int(ogr,2) * int(csr,2)

inputs = getInputs(INPUTREAL)

'''Part One'''
mcb = getMostCommonBits(inputs)
rate = getGammaEpsilon(mcb)
print(rate)

'''Part Two'''
mostCommonBits = getCommonBitsCurrent(inputs,0,True)
leastCommonBits = getCommonBitsCurrent(inputs,0,False)
lsr = getLifeSupportRating(mostCommonBits,leastCommonBits)
print(lsr)