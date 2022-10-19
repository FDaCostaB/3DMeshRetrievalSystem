import sys
import DBData as db
from featureName import featureName, featureDimension
import os
from Features import FeaturesExtract
from Mesh import Mesh

if len(sys.argv) == 1:
    db.normalization()
    db.plotHistogram('remesh')
    db.plotHistogram('output')
elif len(sys.argv) == 2:
    db.drawCategoryFeatures(sys.argv[1], [featureName.COMPACTNESS.value])
    # feature = FeaturesExtract(sys.argv[1])
    # feature.showBoundingBox()

    # ms = Mesh(sys.argv[1])
    # feature = FeaturesExtract(sys.argv[1])
    # print(feature.surfaceArea())

    # ms = Mesh(sys.argv[1])
    # ms.resample()
    # ms.saveMesh()
    # ms.render()

elif len(sys.argv) == 3:
    if sys.argv[1] == "analyze":
        m = Mesh(sys.argv[2])
        print(m.dataFilter())

    if sys.argv[1] == "statistics":
        db.exportDirData(sys.argv[2])

    if sys.argv[1] == "histograms":
        db.histograms(sys.argv[2])