import copy
from queue import PriorityQueue
'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'
IS = 'inputsample.txt'

class Graph():
    def __init__(self,nodes):
        self.vertices = []
        self.nodes = nodes
        self.vertNames = []
        for i in range(len(nodes)):
            currentRow = []
            for j in range(len(nodes[0])):
                currentRow.append(Vertex(f'{i},{j}'))
                self.vertNames.append(f'{i},{j}')
            self.vertices.append(currentRow)
        self.addEdges()
    def addEdges(self):
        rows = len(self.nodes)
        cols = len(self.nodes[0])
        for i in range(rows):
            for j in range(cols):
                if i - 1 >= 0:
                    self.vertices[i][j].addEdge(self.vertices[i-1][j],self.nodes[i-1][j])
                if i + 1 <= rows -1:
                    self.vertices[i][j].addEdge(self.vertices[i+1][j],self.nodes[i+1][j])
                if j - 1 >= 0:
                    self.vertices[i][j].addEdge(self.vertices[i][j-1],self.nodes[i][j-1])
                if j + 1 <= cols - 1:
                    self.vertices[i][j].addEdge(self.vertices[i][j+1],self.nodes[i][j+1])
    def printVertices(self):
        for row in self.vertices:
            rowNames = []
            for v in row:
                rowNames.append(v.name)
            print(rowNames)
    def getVertex(self,v):
        return self.vertDict[v]
    def buildVertexDict(self):
        self.vertDict = {}
        for row in self.vertices:
            for vert in row:
                self.vertDict[vert.name] = vert
    def findSmallestDistance(self,distances,visited):
        # d = copy.copy(distances)
        # for v in visited:
        #     del d[v]
        # invDist = { v: k for k,v in d.items() }
        # i = 0
        # smallest = ''
        # foundSmallest = False
        # while not foundSmallest:
        #     if i in invDist:
        #         smallest = invDist[i]
        #         foundSmallest = True
        #     i += 1
        # return smallest
        distance = float('inf')
        smallest = ''
        for key, value in distances.items():
            if value < distance and not visited[key]:
                smallest = key
                distance = value
        return smallest
    def dijkstra(self,start,finish):
        self.buildVertexDict()
        distances = { x : float('inf') for x in self.vertNames}
        distances[start] = 0
        visited = {x : False for x in self.vertNames }
        unvisited = list(distances.keys())
        q = PriorityQueue()
        q.put((distances[start],start))

        while unvisited:
            newQ = copy.copy(q)
            currentVertex = ''
            dist, name = q.get()
            while visited[name] == True:
                dist, name = newQ.get()
            currentVertex = self.getVertex(name)
            for neighbor in currentVertex.edges:
                nName = neighbor[0].name
                nDistance = neighbor[1]
                currentVertextDist = distances[currentVertex.name]
                if not visited[nName]:
                    if nDistance + currentVertextDist < distances[nName]:
                        distances[nName] = nDistance + currentVertextDist
                    q.put((nDistance + currentVertextDist, nName))
                visited[currentVertex.name] = True
            unvisited.pop(unvisited.index(currentVertex.name))
        return distances[finish]


class Vertex:
    def __init__(self,vertexName):
        self.edges = []
        self.name = vertexName
    def addEdge(self,end,weight):
        self.edges.append([end,weight])
    def isVAdjacentTo(self,v):
        for u in self.edges:
            if u[0].name == v:
                return True
        return False
    def getDistanceTo(self,v):
        for u in self.edges:
            if u[0].name == v:
                return u[1]
        return None

def addNToEach(matrix,n):
    newMatrix = []
    for row in matrix:
        newRow = []
        for col in row:
            newRow.append(col + n - 9 if col + n > 9 else col + n)
        newMatrix.append(newRow)
    return newMatrix

def extendMatrix(m):
    mNew = copy.copy(m)
    for i in range(4):
        mToAdd = addNToEach(m,i + 1)
        for i in range(len(mNew)):
            mNew[i] = mNew[i] + mToAdd[i]
    m = copy.copy(mNew)
    for i in range(4):
        mToAdd = addNToEach(m, i + 1)
        mNew = mNew + mToAdd
    return mNew

def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    matrix = []
    for line in lines:
        line = [int(x) for x in list(line.strip())]
        matrix.append(line)
    file.close()
    return matrix

m = getInputs(INPUTREAL)
'''Part One'''
g = Graph(m)
rows = len(m)
cols = len(m[0])
minLength = g.dijkstra('0,0',f'{rows-1},{cols-1}')
print(minLength)


'''Part Two'''
m = extendMatrix(m)
g = Graph(m)
rows = len(m)
cols = len(m[0])
minLength = g.dijkstra('0,0',f'{rows-1},{cols-1}')
print(minLength)