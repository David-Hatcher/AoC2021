'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    inputs = []
    for line in lines:
        inputs.append(list(line.strip()))
    file.close()
    return inputs

def printList(list):
    for item in list:
        print(item)

def checkSyntaxOfLine(line):
    bracketsStack = []
    openingBrackets = ['(','[','{','<']
    closingBrackets = [')',']','}','>']
    for char in line:
        if char in openingBrackets:
            bracketsStack.insert(0,char)
        else:
            lastOpeningBracket = bracketsStack.pop(0)
            expectedCharacter = closingBrackets[openingBrackets.index(lastOpeningBracket)]
            if closingBrackets.index(char) != openingBrackets.index(lastOpeningBracket):
                return False, char, expectedCharacter, None
    charactersToCompleteLine = [closingBrackets[openingBrackets.index(bracket)] for bracket in bracketsStack]
    return True, None, None, charactersToCompleteLine

def getIllegalCharValue(char):
    if char == ')':
        return 3
    elif char == ']':
        return 57
    elif char == '}':
        return 1197
    elif char == '>':
        return 25137
    else:
        return None

def checkLinesForSyntaxErrors(lines):
    badCharacters = []
    charactersNeededToFinish = []
    for line in lines:
        isListGood, badCharacter, expectedCharacter, leftOverCharacters = checkSyntaxOfLine(line)
        if not isListGood:
            print(f'Expected {expectedCharacter}, but found {badCharacter} instead')
            badCharacters.append(badCharacter)
        else:
            print(f'Characters needed to finish = {leftOverCharacters}')
            charactersNeededToFinish.append(leftOverCharacters)
    return badCharacters, charactersNeededToFinish

def getErrorScores(badCharacters):
    scoreCount = 0
    for character in badCharacters:
        score = getIllegalCharValue(character)
        if score != None:
            scoreCount += score
    return scoreCount

def getClosingCharValue(char):
    if char == ')':
        return 1
    elif char == ']':
        return 2
    elif char == '}':
        return 3
    elif char == '>':
        return 4
    else:
        return 0

def getScoreForNeeded(characters):
    multValue = 5
    totalScore = 0
    for char in characters:
        totalScore = totalScore * multValue
        totalScore += getClosingCharValue(char)
    return totalScore

def getCharactersNeededScores(characterLists):
    scores = []
    for characterList in characterLists:
        score = getScoreForNeeded(characterList)
        scores.append(score)
    return scores

def getMiddleValue(values):
    sortedValues = sorted(values)
    middleValue = int(len(values)/2)
    return sortedValues[middleValue]

bracketLists = getInputs(INPUTREAL)

'''Part One'''
badCharacters, charactersNeeded = checkLinesForSyntaxErrors(bracketLists)
errorScore = getErrorScores(badCharacters)
print(errorScore)


'''Part Two'''
scores = getCharactersNeededScores(charactersNeeded)
middleScore = getMiddleValue(scores)
print(middleScore)