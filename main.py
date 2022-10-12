import sys
from FileIO import normaliseDB, plotDB, viewCategory,normCategory
from Mesh import Mesh

if len(sys.argv) == 1:
    normaliseDB(5000, 200)
    plotDB('Models')
    plotDB('output')
elif len(sys.argv) == 2:
    normCategory(sys.argv[1], 5000, 200)
    viewCategory(sys.argv[1], 'diagonal', True)
    # ms = Mesh(sys.argv[1])
    # ms.render()
    # ms.silhouetteExport()
    # ms.resample(10000, 1000, True)
