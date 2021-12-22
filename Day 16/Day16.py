'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

conversionDict = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'A' : '1010',
    'B' : '1011',
    'C' : '1100',
    'D' : '1101',
    'E' : '1110',
    'F' : '1111'
}

def getInputs(fileName):
    file = open(fileName)
    line = file.readline()
    file.close()
    bitString = []
    for x in line:
        bitString.extend(list(conversionDict[x]))
    return bitString

def getIntFromBits(start,length):
    return int(''.join(packet[start:start+length]),2)

def getLiteral(currentIndex):
    literalString = []
    lastLiteral = False
    while not lastLiteral:
        if packet[currentIndex] == '0':
            lastLiteral = True
        literalString.extend(packet[currentIndex+1:currentIndex+5])
        currentIndex += 5
    return int(''.join(literalString),2),currentIndex

def getPacketHeader(currentIndex):
    return getIntFromBits(currentIndex,3), getIntFromBits(currentIndex+3,3), currentIndex+6

def summationOperation(values):
    return sum(values)

def productOperation(values):
    finalValue = 1
    for value in values:
        finalValue *= value
    return finalValue

def minimumOperation(values):
    return min(values)

def maximumOperation(values):
    return max(values)

def greaterThanOperation(values):
    if values[0] > values[1]:
        return 1
    return 0

def lessThanOperation(values):
    if values[0] < values[1]:
        return 1
    return 0

def equalsOperation(values):
    if values[0] == values[1]:
        return 1
    return 0

def performOperation(opCode,values):
    if opCode == 0:
        return summationOperation(values)
    elif opCode == 1:
        return productOperation(values)
    elif opCode == 2:
        return minimumOperation(values)
    elif opCode == 3:
        return maximumOperation(values)
    elif opCode == 5:
        return greaterThanOperation(values)
    elif opCode == 6:
        return lessThanOperation(values)
    elif opCode == 7:
        return equalsOperation(values)

def parseOpPacket(opCode,currentIndex):
    literals = []
    if packet[currentIndex] == '0':
        countNextBits = 15
        subPacketLength = getIntFromBits(currentIndex + 1, countNextBits)
        currentIndex += countNextBits + 1
        endOfCurrentSubpacket = currentIndex + subPacketLength
        while currentIndex < endOfCurrentSubpacket:
            result, currentIndex = parsePacket(currentIndex)
            literals.append(result)
    else:
        countNextBits = 11
        packetCount = getIntFromBits(currentIndex+1, countNextBits)
        currentIndex += countNextBits + 1
        for _ in range(packetCount):
            result, currentIndex = parsePacket(currentIndex)
            literals.append(result)
    return performOperation(opCode,literals), currentIndex


def parsePacket(currentIndex):
    version, typeId, currentIndex = getPacketHeader(currentIndex)
    versionNumbers.append(version)
    if typeId == 4:
        results, currentIndex = getLiteral(currentIndex)
    else:
        results, currentIndex = parseOpPacket(typeId,currentIndex)
    return results, currentIndex

packet = getInputs(INPUTREAL)
versionNumbers = []
total, currentIndex = parsePacket(0)
'''Part One'''
print(f'version sum: {sum(versionNumbers)}')

'''Part Two'''
print(f'total: {total}')