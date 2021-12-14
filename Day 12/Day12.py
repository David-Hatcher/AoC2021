import copy

'''Global Defs'''
INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

class Graph:
    def __init__(self, vertcies):
        self.root = ''
        self.vertices = []
        self.end = ''
        self.buildNodes(vertcies)
        self.setStart()
        self.setEnd()
        self.visitedTwice = False
    def buildNodes(self,vertices):
        for vertex in vertices:
            self.vertices.append(Vertex(vertex))
    def getVerticies(self):
        return self.vertices
    def setStart(self):
        self.root = self.findVertex('start')
    def setEnd(self):
        self.end = self.findVertex('end')
    def addEdges(self,edges):
        for edge in edges:
            start = self.findVertex(edge[0])
            end = self.findVertex(edge[1])
            start.addEdge(end)
            end.addEdge(start)
            pass
    def findVertex(self,name):
        for vertex in self.vertices:
            if vertex.name == name:
                return vertex
    def findPathsRecur(self, s, e, visited, path, paths):
        visited[s.name] = True
        path.append(s.name)
        if s.name == e.name:
            paths.append(copy.copy(path))
        else:
            for i in s.edges:
                if visited[i.name] == False or i.name.upper() == i.name:
                    self.findPathsRecur(i, e, visited, path, paths)
        path.pop()
        visited[s.name] = False

    def findPathsRecurTwo(self, s, e, visited, path, paths, smallCaveToVisitTwice):
        visited[s.name] += 1
        path.append(s.name)
        if s.name == e.name:
            paths.append(copy.copy(path))
        else:
            for i in s.edges:
                if visited[i.name] == 0 or i.name.upper() == i.name or (i.name == smallCaveToVisitTwice and visited[i.name] == 1):
                    self.findPathsRecurTwo(i, e, visited, path, paths, smallCaveToVisitTwice)
        path.pop()
        visited[s.name] -= 1


    def findPaths(self):
        path = []
        paths = []
        visisted = { x.name : False for x in self.vertices}
        self.findPathsRecur(self.root, self.end, visisted, path, paths)
        return paths, len(paths)

    def findPathsTwo(self):
        pathsFull = {}
        smallCaves = self.getSmallCaves()
        for smallCaveToVisitTwice in smallCaves:
            paths = []
            path = []
            visitedCount = { x.name : 0 for x in self.vertices}
            self.findPathsRecurTwo(self.root, self.end, visitedCount, path, paths, smallCaveToVisitTwice)
            for path in paths:
                key = ','.join(path)
                if key not in pathsFull:
                    pathsFull[key] = 1
        return pathsFull, sum(pathsFull.values())

    def getSmallCaves(self):
        smallCaves = []
        for vertex in self.vertices:
            if vertex.name != 'start' and vertex.name != 'end' and vertex.name.upper() != vertex.name:
                smallCaves.append(vertex.name)
        return smallCaves

class Vertex:
    def __init__(self,vertexName):
        self.edges = []
        self.name = vertexName
    def addEdge(self,end):
        self.edges.append(end)


def getInputs(fileName):
    file = open(fileName,'r')
    lines = file.readlines()
    vertices = set()
    edges = []
    for line in lines:
        nodes = line.strip().split('-')
        vertices.add(nodes[0])
        vertices.add(nodes[1])
        edges.append(nodes)
    file.close()
    return vertices, edges

v, e = getInputs(INPUTREAL)
g = Graph(v)
g.addEdges(e)

'''Part One'''
paths, pathCount = g.findPaths()
print(pathCount)


'''Part Two'''
pathsTwo, pathsCountTwo = g.findPathsTwo()
print(pathsCountTwo)