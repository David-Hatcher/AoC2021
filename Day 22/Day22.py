from itertools import product
'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

'''on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10'''

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    file.close()
    cubeList = []
    for line in lines:
        line = line.strip().split(' ')
        command = line[0]
        coords = line[1].split(',')
        rangeDict = {}
        for coord in coords:
            axis = coord.split('=')[0]
            rangeDict[axis] = {}
            values = [ int(i) for i in coord.split('=')[1].split('..') ]
            rangeDict[axis]['min'] = int(values[0])
            rangeDict[axis]['max'] = int(values[1])
        cubeList.append([True if command == 'on' else False,rangeDict])
    return cubeList

def markMap(dict,switchRanges,maxValue=50,minValue=-50,):
    on = switchRanges[0]
    ranges = switchRanges[1]
    minMin = min(ranges['x']['min'], ranges['y']['min'], ranges['z']['min'])
    maxMax = max(ranges['x']['max'], ranges['y']['max'], ranges['z']['max'])
    if minMin < minValue or maxMax > maxValue:
        return
    xRanges = [x for x in range(ranges['x']['min'], ranges['x']['max'] + 1)]
    yRanges = [y for y in range(ranges['y']['min'], ranges['y']['max'] + 1)]
    zRanges = [z for z in range(ranges['z']['min'], ranges['z']['max'] + 1)]

    cubes = product(xRanges,yRanges,zRanges)
    for cube in cubes:
        dict[f'{cube[0]},{cube[1]},{cube[2]}'] = on

def countOnCubes(dict):
    return list(dict.values()).count(True)

commands = getInputs(INPUTREAL)

mapDict = {}
print(f'Total Number of Commands = {len(commands)}')
for command in commands:
    markMap(mapDict,command)


onCount = countOnCubes(mapDict)
print(onCount)