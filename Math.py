import numpy as np


def dist(a, b):
    x = 0
    y = 1
    z = 2
    return ((b[x] - a[x])**2 + (b[y] - a[y])**2 + (b[z] - a[z])**2)**0.5


def length(vect):
    return dist(vect, [0, 0, 0])


def triangleArea(a, b, c):
    return triangleAreaVector(vect(a,b),vect(a,c))


def triangleAreaVector(vectA, vectB):
    return length(crossProduct(vectA, vectB))/2


def dotProduct(vectA, vectB):
    return vectA[0] * vectB[0] + vectA[1] * vectB[1] + vectA[2] * vectB[2]


def crossProduct(vectA, vectB):
    return [vectA[1] * vectB[2] - vectA[2] * vectB[1], vectA[2] * vectB[0] - vectA[0] * vectB[2], vectA[0] * vectB[1] - vectA[1] * vectB[0]]


def angle(vectA, vectB):
    similarity = dotProduct(vectA, vectB) / (length(vectA) * length(vectB))
    if similarity < -1 : similarity = -1
    if similarity > 1 : similarity = 1
    return np.arccos(similarity)


def tetrahedronVolume(vectA, vectB, vectC):
    return dotProduct(crossProduct(vectA, vectB), vectC) / 6


def vect(vectA, vectB):
    return [vectB[0] - vectA[0], vectB[1] - vectA[1], vectB[2] - vectA[2]]
