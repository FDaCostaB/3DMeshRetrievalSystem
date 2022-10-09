import sys
from FileIO import normaliseDB, plotDB
from Mesh import Mesh

if len(sys.argv) == 1:
    # normaliseDB(10000, 1000)
    plotDB('Models')
    # plotDB('output')
elif len(sys.argv) == 2:
    ms = Mesh(sys.argv[1])
    ms.render()
    # ms.resample(10000, 1000, True)

