import numpy as np


def dist(a, b):
    x = 0
    y = 1
    z = 2
    return ((b[x] - a[x])**2 + (b[y] - a[y])**2 + (b[z] - a[z])**2)**0.5


def length(v):
    return dist(v, [0, 0, 0])


def triangleArea(a, b, c):
    ab = dist(a, b)
    bc = dist(b, c)
    ac = dist(a, c)
    s = (ab+bc+ac) / 2
    area = (s*(s-ab)*(s-bc)*(s-ac))**0.5
    return area


def triangleAreaVector(a, b):
    return length(crossProduct(a, b))/2


def dotProduct(a, b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


def crossProduct(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def angle(a, b):
    return np.arccos(dotProduct(a, b)/length(a)*length(b))


def tetrahedronVolume(a, b, c):
    return dotProduct(crossProduct(a, b), c)/6


def vect(a, b):
    return [b[0]-a[0], b[1]-a[1], b[2]-a[2]]
