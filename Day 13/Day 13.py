import copy
import numpy as np

'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'


def getInputs(fileName):
    folds = []
    points = []
    file = open(fileName,'r')
    lines = file.readlines()
    readingInstructions = False
    for line in lines:
        if line.strip() == '':
            readingInstructions = True
            continue
        if not readingInstructions:
            pointCoords = line.strip().split(',')
            points.append({ 'x' : int(pointCoords[0]) , 'y' : int(pointCoords[1])})
        else:
            line = line.strip().split(' ')
            foldInstructions = line[2].split('=')
            folds.append({'axis' : foldInstructions[0], 'point' : int(foldInstructions[1])})
    return points, folds

def getMaxValues(points):
    xMax, yMax = 0,0
    for point in points:
        if point['x'] > xMax:
            xMax = point['x']
        if point['y'] > yMax:
            yMax = point['y']
    return xMax + 1, yMax + 1

def makeStartingPaper(rows,cols):
    paper = []
    for _ in range(cols):
        paper.append(['.'] * rows)
    return paper

def printPaper(paper):
    for row in paper:
        print(''.join(row))

def markPaper(paper,points):
    for point in points:
        paper[point['y']][point['x']] = '#'

def countMarks(paper):
    marksCount = 0
    for i in range(len(paper)):
        for j in range(len(paper[0])):
            if paper[i][j] == '#':
                marksCount += 1
    return marksCount

def foldPaper(paper,fold):
    firstPart = []
    secondPart = []
    if fold['axis'] == 'y':
        firstPart = paper[0:fold['point']]
        secondPart = paper[fold['point'] + 1:]
        secondPart = secondPart[::-1]
        currentRow = -1
        while secondPart:
            currentLine = secondPart.pop(-1)
            for i in range(len(currentLine)):
                if firstPart[currentRow][i] != '#':
                    firstPart[currentRow][i] = currentLine[i]
            currentRow -= 1
    if fold['axis'] == 'x':
        for row in paper:
            firstPart.append(row[0:fold['point']])
            secondPart.append(row[fold['point'] + 1:])
        for i in range(len(secondPart)):
            for j in range(len(secondPart[0])):
                if firstPart[i][-1-j] != '#':
                    firstPart[i][-1-j] = secondPart[i][j]
    return firstPart


points, folds = getInputs(INPUTREAL)
rows, cols = getMaxValues(points)

paper = makeStartingPaper(rows,cols)

'''Part One'''
paperPartOne = copy.copy(paper)
markPaper(paperPartOne,points)
paperPartOne = foldPaper(paperPartOne,folds[0])
marksCount = countMarks(paperPartOne)
print(marksCount)

'''Part Two'''
paperPartTwo = copy.copy(paper)
markPaper(paperPartTwo,points)
for fold in folds:
    paperPartTwo = foldPaper(paperPartTwo,fold)
printPaper(paperPartTwo)