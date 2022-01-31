import os,itertools
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

def getInput(fileName):
    enhAlgo = []
    image = []
    file = open(fileName,'r')
    enhAlgo = [x for x in file.readline().rstrip()]
    file.readline()
    lines = file.readlines()
    for line in lines:
        image.append([x for x in line.rstrip()])
    return enhAlgo, image

def getOnPixelCount(fileName, times):
    enhAlgo, image = getInput(fileName)

    dirs = list(itertools.product([-1,0,1], [-1,0,1]))
    infSpace = "0"

    for _ in range(times):
        rows = len(image)
        cols = len(image[0])
        enhImage = [['.' for _ in range(cols + 2)] for _ in range(rows + 2)]
        for row in range(-1, rows + 1):
            for col in range(-1, cols + 1):
                pixel = ""
                for rc, cc in dirs:
                    currRow = row + rc
                    currCol = col + cc
                    if 0 <= currRow < rows and 0 <= currCol < cols:
                        pixel += "1" if image[currRow][currCol] == "#" else "0"
                    else:
                        pixel += infSpace
                enhImage[row + 1][col + 1] = enhAlgo[int(pixel, 2)]
        infSpace = "1" if enhAlgo[int((infSpace * 9), 2)] == "#" else "0"
        image = enhImage

    return sum([line.count("#") for line in image])

'''Part One'''
print(getOnPixelCount('input.txt', 2))

'''Part Two'''
print(getOnPixelCount('input.txt', 50))