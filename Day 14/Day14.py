import copy
'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'


def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    template = lines.pop(0).strip()
    lines.pop(0)
    replaceDict = {}
    for line in lines:
        lineArr = line.strip().split(' -> ')
        replaceDict[lineArr[0]] = lineArr[1]
    file.close()
    return template, replaceDict

def processTemplate(replaceDict,pairCountDict,characterCountsDict):
    newCountDict = copy.copy(pairCountDict)
    for key, value in pairCountDict.items():
        if value > 0:
            newCountDict[key[0] + replaceDict[key]] += value
            newCountDict[replaceDict[key] + key[1]] += value
            newCountDict[key] -= value
            try:
                characterCountsDict[replaceDict[key]] += value
            except:
                characterCountsDict[replaceDict[key]] = value
    return newCountDict

def createCountDict(template,replaceDict):
    characterCountDict = {}
    pairCountDict = { x : 0 for x in replaceDict.keys()}
    for i in range(len(template) -1):
        try:
            characterCountDict[template[i]] += 1
        except:
            characterCountDict[template[i]] = 1
        twoChar = template[i:i+2]
        pairCountDict[twoChar] += 1
    try:
        characterCountDict[template[-1]] += 1
    except:
        characterCountDict[template[-1]] = 1
    return pairCountDict, characterCountDict

def findMostMinusLeast(counts):
    return max(counts.values()) - min(counts.values())


'''Part One'''
template, replaceDict = getInputs(INPUTREAL)
pairCountsDict, characterCounts = createCountDict(template,replaceDict)
for _ in range(10):
    pairCountsDict = processTemplate(replaceDict,pairCountsDict,characterCounts)
print(findMostMinusLeast(characterCounts))

'''Part Two'''
for _ in range(30):
    pairCountsDict = processTemplate(replaceDict,pairCountsDict,characterCounts)
print(findMostMinusLeast(characterCounts))