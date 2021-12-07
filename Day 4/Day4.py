import numpy as np
'''Global Defs'''

INPUTREAL = 'input.txt'
INPUTTEST = 'inputtest.txt'

def removeEmptyValuesFromArr(arr):
    return [int(value) for value in arr if value != '']

def getInput(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    numbers = lines[0].strip().split(',')
    lines = lines[2:]
    boards = []
    n = 5
    currentBoard = []
    for line in lines:
        currentLine = removeEmptyValuesFromArr(line.strip().split(' '))
        if currentLine != []:
            currentBoard.append(currentLine)
        if line == '\n':
            boards.append(currentBoard)
            currentBoard = []
            continue
    boards.append(currentBoard)
    return numbers, boards

def buildBoards(boards):
    newBoards = []
    for board in boards:
        currentBoard = []
        for row in board:
            currentRow = []
            for num in row:
                currentRow.append([num,False])
            currentBoard.append(currentRow)
        newBoards.append(currentBoard)
    return newBoards

def checkForWinner(board):
    rows = columns = 5
    arr = np.array(board)
    # print(arr)
    '''Check Rows'''
    for i in range(rows):
        currentRow = arr[i,:]
        val = np.sum(currentRow,0)[1]
        if val == rows:
            return True
    '''Check Columns'''
    for i in range(columns):
        currentColumn = arr[:,i]
        val = np.sum(currentColumn,0)[1]
        if val == columns:
            return True
    return False

def markNumber(board,number):
    rows = columns = 5
    for i in range(rows):
        for j in range(columns):
            if board[i][j][0] == number:
                board[i][j][1] = True

def getUnmarkedCount(board):
    count = 0
    rows = columns = 5
    for i in range(rows):
        for j in range(columns):
            if not board[i][j][1]:
                count += board[i][j][0]
    return count

numbers, boards = getInput(INPUTREAL)

boards = buildBoards(boards)

'''Part One'''
winnerFound = False
winningBoard = ''
winningNumber = 0
for number in numbers:
    if winnerFound:
        break
    for board in boards:
        markNumber(board,int(number))
    for board in boards:
        currentBoardIsWinner = checkForWinner(board)
        if currentBoardIsWinner:
            winnerFound = True
            winningBoard = board
            winningNumber = int(number)



unmarkedCount = getUnmarkedCount(winningBoard)

print(unmarkedCount*winningNumber)

'''Part Two'''
winnerArray = [0 for board in boards]
winningBoard = ''
winningNumber = 0
lastWinner =''
for number in numbers:
    for board in boards:
        markNumber(board,int(number))
    for i in range(len(boards)):
        if winnerArray[i] != 1:
            currentBoardIsWinner = checkForWinner(boards[i])
            if currentBoardIsWinner:
                winningBoard = boards[i]
                winnerArray[i] = 1
    if winnerArray.count(1) == len(winnerArray):
        lastWinner = winningBoard
        winningNumber = int(number)
        break

unmarkedCount = getUnmarkedCount(lastWinner)
print(unmarkedCount*winningNumber)

