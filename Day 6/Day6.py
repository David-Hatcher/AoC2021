'''Global Defs'''
INPUTREAL = 'input.txt'
INPUTTEST = 'inputtest.txt'


def getInputs(fileName):
    file = open(fileName,'r')
    line = [int(x) for x in file.readline().strip().split(',')]
    file.close()
    return line

def passDaysSlow(fishes):
    currentFishesCount = len(fishes)
    for i in range(currentFishesCount):
        if fishes[i] == 0:
            fishes[i] = 6
            fishes.append(8)
        else: 
            fishes[i] -= 1
    return fishes

def passDaysFast(fishes,days):
    d = { x : 0 for x in range(9) }
    fishSet = set(fishes)
    for fish in fishSet:
        d[fish] += fishes.count(fish)
    for _ in range(days):
        a = {}
        a[8] = d[0]
        a[7] = d[8]
        a[6] = d[7] + d[0]
        a[5] = d[6]
        a[4] = d[5]
        a[3] = d[4]
        a[2] = d[3]
        a[1] = d[2]
        a[0] = d[1]
        d = a
    fishSum = 0
    for key, value in d.items():
        fishSum += value
    return fishSum

fishesInit = getInputs(INPUTREAL)

'''Part One'''
fishes = passDaysFast(fishesInit,80)
print(fishes)

'''Part Two'''
fishes = passDaysFast(fishesInit,256)
print(fishes)