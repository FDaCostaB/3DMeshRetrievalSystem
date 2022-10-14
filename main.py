import sys
import DBData as db
from featureName import featureName, featureDimension
import os
from Features import FeaturesExtract
from Mesh import Mesh

if len(sys.argv) == 1:
    # db.normalise()
    db.plot('remesh')
    db.plot('output')
elif len(sys.argv) == 2:
    db.drawCategoryFeatures(sys.argv[1], [featureName.RECTANGULARITY.value])
    # ms = Mesh(sys.argv[1])
    # ms.resample()
    # ms.saveMesh("./initial")

    # ms = Mesh(sys.argv[1])
    # feature = FeaturesExtract(sys.argv[1])
    # print(feature.surfaceArea())

    # db.normCategory(sys.argv[1])
    # db.viewCategory(sys.argv[1], 'diagonal', True)

    # ms = Mesh(sys.argv[1])
    # ms.resample()
    # ms.render()
    # ms.saveMesh()
