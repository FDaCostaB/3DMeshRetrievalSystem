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
    db.drawCategoryFeatures(sys.argv[1], [featureName.ECCENTRICITY.value])
    # feature = FeaturesExtract(sys.argv[1])
    # feature.showBoundingBox()

    # ms = Mesh(sys.argv[1])
    # feature = FeaturesExtract(sys.argv[1])
    # print(feature.surfaceArea())

    # ms = Mesh(sys.argv[1])
    # ms.resample()
    # ms.saveMesh()
    # ms.render()