'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

def getInputsPartOne(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    commands = {}
    for line in lines:
        direction = line.split(' ')[0]
        magnitude = int(line.split(' ')[1])
        try:
            commands[direction] += magnitude
        except:
            commands[direction] = magnitude
    return commands

def getInputsPartTwo(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    commands = []
    for line in lines:
        direction = line.split(' ')[0]
        magnitude = int(line.split(' ')[1])
        commands.append((direction,magnitude))
    return commands

def getHoriTimesDepth(dist):
    depth = dist['down'] - dist['up']
    hori = dist['forward']
    return depth * hori

def getDist(inputs):
    aim = 0
    depth = 0
    horiDist = 0
    for command in inputs:
        if command[0] == 'down':
            aim += command[1]
        elif command[0] == 'up':
            aim -= command[1]
        elif command[0] == 'forward':
            depth += aim * command[1]
            horiDist += command[1]
    return horiDist * depth

# inputs = getInputs(_inputTest)

'''Part One'''
inputsPartOne = getInputsPartOne(INPUTREAL)
value = getHoriTimesDepth(inputsPartOne)
print(value)

'''Part Two'''
inputsPartTwo = getInputsPartTwo(INPUTREAL)
value = getDist(inputsPartTwo)
print(value)