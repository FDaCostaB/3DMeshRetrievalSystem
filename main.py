import sys
import DBData as db
from Mesh import Mesh

if len(sys.argv) == 1:
    db.normalise(5000, 200)
    db.plot('Models')
    db.plot('output')
elif len(sys.argv) == 2:
    # io.normCategory(sys.argv[1], 5000, 200)
    # io.viewCategory(sys.argv[1], 'diagonal', True)
    ms = Mesh(sys.argv[1])
    # ms.render()
    # ms.silhouetteExport()
    ms.resample(5000, 1000, True)
