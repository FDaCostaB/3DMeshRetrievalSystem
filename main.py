import sys
import DBData as db
from Mesh import Mesh

if len(sys.argv) == 1:
    # db.normalise()
    db.plot('remesh')
    db.plot('output')
elif len(sys.argv) == 2:
    # db.normCategory(sys.argv[1])
    db.viewCategory(sys.argv[1], 'diagonal', True)
    # ms = Mesh(sys.argv[1])
    # ms.render()
    # ms.silhouetteExport()
    # ms.resample(5000, 1000, True)
