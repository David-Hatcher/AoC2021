from itertools import product

'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'


def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    file.close()
    startingSpaces = []
    for line in lines:
        startingSpaces.append(int(line.strip().split(': ')[1]))
    return startingSpaces

class Game:
    def __init__(self, pOnePos, pTwoPos, dice):
        self.turn = 1
        self.pOneScore = 0
        self.pTwoScore = 0
        self.pOnePos = pOnePos
        self.pTwoPos = pTwoPos
        self.dice = dice

    def runTurn(self,numOfRolls=3):
        rolls = [self.dice.roll() for _ in range(numOfRolls)]
        moveCount = sum(rolls)

        if self.turn == 1:
            self.pOnePos = (self.pOnePos + moveCount - 1) % 10 + 1
            self.pOneScore += self.pOnePos
            self.turn = 2
        elif self.turn == 2:
            self.pTwoPos = (self.pTwoPos + moveCount - 1) % 10 + 1
            self.pTwoScore += self.pTwoPos
            self.turn = 1

    def winnerFound(self):
        if self.pOneScore >= 1000:
            return 1
        elif self.pTwoScore >= 1000:
            return 2
        else:
            return 0

    def getNumberOfRolls(self):
        return self.dice.rollCount


class Dice:
    def __init__(self):
        self.current = 1
        self.rollCount = 0

    def roll(self):
        roll = self.current
        self.rollCount += 1
        self.current = self.current % 100 + 1
        return roll

starting = getInputs(INPUTREAL)
g = Game(starting[0], starting[1], Dice())

while True:
    g.runTurn()
    winner = g.winnerFound()
    if winner != 0:
        if winner == 2:
            print("Player One loses, score =", g.pOneScore, "Losing score * Roll Count =", g.pOneScore * g.getNumberOfRolls())
        else:
            print("Player Two loses, Score =", g.pTwoScore, "Losing Score * Roll Count =", g.pTwoScore * g.getNumberOfRolls())
        break


'''Part Two'''
winsDict = {}
turnDict = {}

def takeTurn(currentPosition,currentScore,roll):
    key = f'{currentPosition}{currentScore}{roll}'
    if key in turnDict:
        return turnDict[key]
    newPosition = (currentPosition + roll - 1) % 10 + 1
    newScore = currentScore + newPosition
    turnDict[key] = [newScore, newPosition]
    return turnDict[key]

'''Memoized function'''
def getWinsCountMemo(player, pOnePos, pOneScore, pTwoPos, pTwoScore):
    key = f'{player}{pOnePos}{pOneScore}{pTwoPos}{pTwoScore}'
    if key in winsDict:
        return winsDict[key]

    if pOneScore >= 21:
        winsDict[key] = [1,0]
        return winsDict[key]
    elif pTwoScore >= 21:
        winsDict[key] = [0,1]
        return winsDict[key]

    wins = [0,0]
    products = product(range(1,4), repeat=3)
    for rolls in products:
        rollSum = sum(rolls)
        if player == 0:
            newScore, newPosition = takeTurn(pOnePos, pOneScore, rollSum)
            pOneWins, pTwoWins = getWinsCountMemo(1, newPosition, newScore, pTwoPos, pTwoScore)
        else:
            newScore, newPosition = takeTurn(pTwoPos, pTwoScore, rollSum)
            pOneWins, pTwoWins = getWinsCountMemo(0, pOnePos, pOneScore, newPosition, newScore)
        wins[0] += pOneWins
        wins[1] += pTwoWins

    winsDict[key] = wins
    return winsDict[key]

wins = getWinsCountMemo(0, starting[0], 0, starting[1], 0)
print(max(wins))
