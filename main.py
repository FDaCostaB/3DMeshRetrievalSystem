import sys
from FileIO import DataIO, normaliseDB
from Debug import debugLvl,debugLog
from Mesh import Mesh
from dataName import dataName


if len(sys.argv) == 1:
    normaliseDB(10000, 1000)

    modelsIO = DataIO('Models')
    modelsIO.plotHistograms(
        [dataName.CATEGORY, dataName.FACE_NUMBERS, dataName.VERTEX_NUMBERS, dataName.SIDE_SIZE, dataName.DIST_BARYCENTER,
         dataName.PCA])

    outputIO = DataIO('output')
    outputIO.plotHistograms(
        [dataName.CATEGORY, dataName.FACE_NUMBERS, dataName.VERTEX_NUMBERS, dataName.SIDE_SIZE, dataName.DIST_BARYCENTER,
         dataName.PCA])
elif len(sys.argv) == 2:
    ms = Mesh(sys.argv[1])
    ms.resample(10000, 1000, True)