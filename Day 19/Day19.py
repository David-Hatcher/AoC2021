from collections import namedtuple, defaultdict
from itertools import combinations, product
from math import sqrt
from typing import List

INPUTTEST = 'inputtest.txt'
INPUTREAL = 'input.txt'

def getLines(fileName):
    file = open(fileName,'r')
    lines = file.read().splitlines()
    file.close()
    return lines


class Point3(namedtuple('Point', 'x y z')):
    def __repr__(self):
        return f'{self.x},{self.y},{self.z}'

# performed x y z rotations in a loop and stored in a set
rotations = [([2, 0, 1], [-1, -1, 1]), ([0, 1, 2], [1, -1, -1]), ([2, 1, 0], [-1, -1, -1]), ([2, 1, 0], [1, -1, 1]),
            ([0, 2, 1], [-1, -1, -1]), ([1, 2, 0], [1, -1, -1]), ([1, 0, 2], [-1, -1, -1]), ([1, 2, 0], [1, 1, 1]),
            ([0, 2, 1], [-1, 1, 1]), ([0, 1, 2], [-1, 1, -1]), ([0, 2, 1], [1, -1, 1]), ([2, 0, 1], [-1, 1, -1]),
            ([1, 0, 2], [1, 1, -1]), ([2, 1, 0], [1, 1, -1]), ([2, 0, 1], [1, 1, 1]), ([2, 1, 0], [-1, 1, 1]),
            ([0, 1, 2], [1, 1, 1]), ([1, 0, 2], [1, -1, 1]), ([1, 0, 2], [-1, 1, 1]), ([0, 1, 2], [-1, -1, 1]),
            ([1, 2, 0], [-1, 1, -1]), ([1, 2, 0], [-1, -1, 1]), ([0, 2, 1], [1, 1, -1]), ([2, 0, 1], [1, -1, -1])]


def formatInput(lines):
    scanners = {}
    scannerCurrent = []
    i = 0
    lines.append("")
    for line in filter(lambda x: not x.startswith("---"), lines):
        if len(line) == 0 and len(scannerCurrent) > 0:
            scanners[i] = scannerCurrent
            scannerCurrent = []
            i += 1
        else:
            scannerCurrent.append([int(t) for t in line.split(",")])
    return scanners


def partOne(scanners):
    intersects = getIntersects(scanners)
    mapping_dict = createMappings(intersects, scanners)
    beacons = set(toPoint(p) for p in scanners[0])
    used_mappings = set()
    transformed_scanners = {0}
    scanner_origins = [[0, 0, 0]]
    while len(transformed_scanners) < len(scanners):
        queue = [k for k in mapping_dict.keys() if k[0] in transformed_scanners and k[1] not in transformed_scanners]
        while len(queue) > 0:
            el = queue.pop()
            if el[1] in transformed_scanners:
                continue
            p_transpose = list(zip(*scanners[el[1]]))
            centroid = list(zip([0, 0, 0]))  # origin relative to scanner itself is 0, 0, 0
            use_mapping = el
            while True:
                centroid = transform(centroid, *mapping_dict[use_mapping])
                p_transpose = transform(p_transpose, *mapping_dict[use_mapping])
                new_points = set(toPoint(p) for p in zip(*p_transpose))
                if use_mapping[0] == 0:
                    break
                for mapping in used_mappings:
                    if mapping[1] == use_mapping[0]:
                        use_mapping = mapping
                        break
            scanner_origins.append([centroid[0][0], centroid[1][0], centroid[2][0]])
            transformed_scanners.add(el[1])
            beacons.update(new_points)
            used_mappings.add(el)
    return len(beacons), scanner_origins


def partTwo(scanner_origins):
    return max(sum(map(lambda x: abs(x[0] - x[1]), zip(*p))) for p in combinations(scanner_origins, 2))


def createMappings(intersects, scanners):
    mappingDict = {}
    for i in intersects:
        pointToDistA = defaultdict(set)
        for p in combinations(scanners[i[0]], 2):
            dist = euclidDist(*p)
            pointToDistA[toPoint(p[0])].add(dist)
            pointToDistA[toPoint(p[1])].add(dist)
        pointToDistB = defaultdict(set)
        for p in combinations(scanners[i[1]], 2):
            dist = euclidDist(*p)
            pointToDistB[toPoint(p[0])].add(dist)
            pointToDistB[toPoint(p[1])].add(dist)
        pointsA = []
        pointsB = []
        for p in product(pointToDistA.keys(), pointToDistB.keys()):
            intersect = pointToDistA[p[0]].intersection(pointToDistB[p[1]])
            if len(intersect) >= 11:  # 12 common beacons 1 src and 11 dst for distance
                pointsA.append(pointToList(p[0]))
                pointsB.append(pointToList(p[1]))
        mappingDict[i] = mapScannerAToB(pointsA, pointsB)
    return mappingDict


def mapScannerAToB(pointsA, pointsB):
    aTranspose = list(zip(*pointsA))
    bTranspose = list(zip(*pointsB))
    for perms, signs in rotations:
        rotated = rotate(bTranspose, perms, signs)
        offset = []
        for p in zip(rotated, aTranspose):
            points = set([x[1] - x[0] for x in zip(p[0], p[1])])
            if len(points) == 1:
                offset.append(points.pop())
            if len(offset) == 3:
                return offset, perms, signs
    return None


def transform(itemToTransform, centerOfTarget, transformPerm, transformSign):
    rotated = rotate(itemToTransform, transformPerm, transformSign)
    return [list(map(lambda x: centerOfTarget[i] + x, p)) for i, p in enumerate(rotated)]


def getIntersects(scanners):
    intersections = []
    distDict = {i: set(euclidDist(*p) for p in combinations(scanners[i], 2)) for i in scanners.keys()}
    for i in combinations(range(len(scanners)), 2):
        if len(distDict[i[0]].intersection(distDict[i[1]])) >= 66:
            intersections.append(i)
            intersections.append((i[1], i[0]))
    return intersections


def rotate(point, perms, signs):
    return map(lambda n: n * signs[0], point[perms[0]]), \
           map(lambda n: n * signs[1], point[perms[1]]), \
           map(lambda n: n * signs[2], point[perms[2]])


def euclidDist(a, b):
    return sqrt(sum(map(lambda x: pow(x[0] - x[1], 2), zip(a, b))))


def toPoint(plist):
    if len(plist) == 3:
        return Point3(plist[0], plist[1], plist[2])
    else:
        raise Exception("Can't cover to point")


def pointToList(p):
    return [p.x, p.y, p.z]


lines = getLines(INPUTREAL)
scanners = formatInput(lines)
part1, centroids = partOne(scanners)
'''Part One'''
print(part1)
'''Part Two'''
print(partTwo(centroids))