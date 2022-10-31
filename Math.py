import numpy as np
from featureName import featureName, histoUpperBound, featureHistoBins

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

def matrixDist(length,histoName):
    matrix = np.zeros( (length, length) )
    for i in range(length):
        for j in range(length):
            matrix[i][j]=(j-i)*histoUpperBound[histoName]/featureHistoBins[histoName]
    return matrix

def standardisation(meshesData):
    avgDict = {'File name': 'avg'}
    stdDict = {'File name': 'std'}
    for key in featureName:
        if key.value[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and key.value not in ['File name', 'Folder name']:
            list = np.array([featureVect[key.value] for featureVect in meshesData])
            avgDict[key.value] = float(list.mean())
            stdDict[key.value] = float(list.std())
    for featuresVect in meshesData:
        for key in featureName:
            if key.value[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and key.value not in ['File name', 'Folder name']:
                featuresVect[key.value] = (featuresVect[key.value] - avgDict[key.value]) / stdDict[key.value]
    meshesData.append(avgDict)
    meshesData.append(stdDict)
    return meshesData

def minMaxNormalisation(meshesData):
    minDict = {'File name': 'min'}
    maxDict = {'File name': 'max'}
    for featuresVect in meshesData:
        for key in featureName:
            if key.value[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and key.value not in ['File name', 'Folder name']:
                list = np.array([featureVect[key.value] for featureVect in meshesData])
                featuresVect[key.value] = (featuresVect[key.value] - min(list)) / (max(list) - min(list))
                minDict[key.value] = min(list)
                maxDict[key.value] = max(list)
    meshesData.append(minDict)
    meshesData.append(maxDict)
    return meshesData