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

class Cuboid:
    def __init__(self,xmin,xmax,ymin,ymax,zmin,zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
    def volume(self):
        return (
            (self.xmax - self.xmin + 1) *
            (self.ymax - self.ymin + 1) *
            (self.zmax - self.zmin + 1)
        )
    def cornerIterator(self):
        for x in [self.xmin, self.xmax]:
            for y in [self.ymin, self.ymax]:
                for z in [self.zmin, self.zmax]:
                    yield (x, y, z)
    def isSmallCube(self):
        for corner in self.cornerIterator():
            for point in corner:
                if abs(point) > 50:
                    return False
        return True
    def doesIntersect(self,cuboidCompare):
        return (
            cuboidCompare.xmin <= self.xmax
            and cuboidCompare.xmax >= self.xmin
            and cuboidCompare.ymin <= self.ymax
            and cuboidCompare.ymax >= self.ymin
            and cuboidCompare.zmin <= self.zmax
            and cuboidCompare.zmax >= self.zmin
        )
    def getIntersection(self,cuboidCompare):
        if not self.doesIntersect(cuboidCompare):
            return None
        return Cuboid(
            max(self.xmin, cuboidCompare.xmin),
            min(self.xmax, cuboidCompare.xmax),
            max(self.ymin, cuboidCompare.ymin),
            min(self.ymax, cuboidCompare.ymax),
            max(self.zmin, cuboidCompare.zmin),
            min(self.zmax, cuboidCompare.zmax),
        )
    def removeParts(self,cuboidCompare):
        newCubes = set()

        # top:
        zmin = cuboidCompare.zmax + 1
        if zmin <= self.zmax:
            newCubes.add(Cuboid(self.xmin, self.xmax, self.ymin, self.ymax, zmin, self.zmax))
            zmin -= 1
        else:
            zmin = self.zmax
        # bottom:
        zmax = cuboidCompare.zmin - 1
        if zmax >= self.zmin:
            newCubes.add(Cuboid(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, zmax))
            zmax += 1
        else:
            zmax = self.zmin

        # right/long:
        xmin = cuboidCompare.xmax + 1
        if xmin <= self.xmax:
            newCubes.add(Cuboid(xmin, self.xmax, self.ymin, self.ymax, zmax, zmin))
            xmin -= 1
        else:
            xmin = self.xmax

        # left/long:
        xmax = cuboidCompare.xmin - 1
        if xmax >= self.xmin:
            newCubes.add(Cuboid(self.xmin, xmax, self.ymin, self.ymax, zmax, zmin))
            xmax += 1
        else:
            xmax = self.xmin

        # back
        ymin = cuboidCompare.ymax + 1
        if ymin <= self.ymax:
            newCubes.add(Cuboid(xmax, xmin, ymin, self.ymax, zmax, zmin))  

        ymax = cuboidCompare.ymin - 1
        if ymax >= self.ymin:
            newCubes.add(Cuboid(xmax, xmin, self.ymin, ymax, zmax, zmin))

        return newCubes

    def removeIntersections(self,cuboidCompare):
        i = self.getIntersection(cuboidCompare)
        if i is None:
            return {self}
        if i == self:
            return set()
        return self.removeParts(i)


def buildCuboids(inputs):
    cuboids = []
    for i in inputs:
        values = i[1]
        c = Cuboid(
            values['x']['min'],
            values['x']['max'],
            values['y']['min'],
            values['y']['max'],
            values['z']['min'],
            values['z']['max']
        )
        cuboids.append([i[0], c])
    return cuboids

def getOnCount(cubes):
    onCubes = set()
    for on, compareCube in cubes:
        newActivatedCubes = set()
        for current in onCubes:
            newActivatedCubes |= current.removeIntersections(compareCube)
        if on:
            newActivatedCubes.add(compareCube)
        onCubes = newActivatedCubes
    return sum(cube.volume() for cube in onCubes)

inputs = getInputs(INPUTREAL)
cubes = buildCuboids(inputs)
smallCubes = filter(lambda x: x[1].isSmallCube(), cubes)
print(getOnCount(smallCubes))
print(getOnCount(cubes))