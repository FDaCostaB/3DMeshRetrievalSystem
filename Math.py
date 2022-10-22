import numpy as np


def dist(a, b):
    if len(a) != len(b):
        raise("Dimmensionality is not the same")

    res = 0
    for i in range(len(a)):
        res += (b[i] - a[i]) ** 2
    return res**0.5


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

def binsArray(leftEdge,rightEdge,nbBins):
    return [leftEdge+i*(rightEdge-leftEdge)/(nbBins+1) for i in range(nbBins+1)]


def matrixDist(length):
    matrix = np.zeros( (length, length) )
    for i in range(length):
        for j in range(length):
            matrix[i][j]=j-i
    return matrix


# http://robotics.stanford.edu/~scohen/research/emdg/emdg-cases.html#T1dL1
# https://gist.github.com/jgraving/db2bf2fab8d623557e26eb363dd91af9
def emd(histA, histB):
    if len(histA) != len(histB):
        raise ("Not same dimensionnality")
    else:
        n = len(histA)
    histACumul = 0
    histBCumul = 0
    diff = 0
    for i in range(n):
        histACumul += histA[i]
        histBCumul += histB[i]
        diff += abs(histACumul - histBCumul) # Without abs the result are the same than pyemd lib given an epsilon=10e-2
    return diff