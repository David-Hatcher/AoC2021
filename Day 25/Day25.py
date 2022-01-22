'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    file.close()
    grid = []
    for line in lines:
        grid.append(list(line.strip()))
    return grid

def moveSlugs(grid):
    checkMovesEast(grid)
    movedEast = moveEast(grid)
    checkMovesSouth(grid)
    movedSouth = moveSouth(grid)
    return movedEast or movedSouth

def checkMovesEast(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j][0] == '>':
                try:
                    if grid[i][j+1][0] == '.':
                        grid[i][j][1] = True
                except:
                    if grid[i][0][0] == '.':
                        grid[i][j][1] = True

def checkMovesSouth(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j][0] == 'v':
                try:
                    if grid[i+1][j][0] == '.':
                        grid[i][j][1] = True
                except:
                    if grid[0][j][0] == '.':
                        grid[i][j][1] = True

def moveSouth(grid):
    slugMoved = False
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            slug = grid[i][j]
            if slug[1] and slug[0] == 'v':
                try:
                    grid[i+1][j][0], slug[0] = slug[0], grid[i+1][j][0]
                except:
                    grid[0][j][0], slug[0] = slug[0], grid[0][j][0]
                slug[1] = False
                slugMoved = True
    return slugMoved

def moveEast(grid):
    slugMoved = False
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            slug = grid[i][j]
            if slug[1] and slug[0] == '>':
                try:
                    grid[i][j+1][0], slug[0] = slug[0], grid[i][j+1][0]
                except:
                    grid[i][0][0], slug[0] = slug[0], grid[i][0][0]
                slug[1] = False
                slugMoved = True
    return slugMoved

def createGrids(grid):
    newGrid = []
    for i in range(len(grid)):
        currentRow = []
        for j in range(len(grid[i])):
            currentRow.append([grid[i][j],False])
        newGrid.append(currentRow)
    return newGrid

def printGrid(grid):
    s = ''
    for row in grid:
        for slug in row:
            s+= slug[0]
        s += '\n'
    print(s)

grid = getInputs(INPUTREAL)
grid = createGrids(grid)
slugsMoved = True
moveCount = 0
while slugsMoved:
    slugsMoved = moveSlugs(grid)
    moveCount += 1
print(f'moveCount = {moveCount}')