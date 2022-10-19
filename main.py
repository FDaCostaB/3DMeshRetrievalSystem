import sys
import DBData as db
from featureName import featureName, featureDimension
import os
from Features import FeaturesExtract
from Mesh import Mesh


if len(sys.argv) == 3:
    if sys.argv[1] == "analyze":
        m = Mesh(sys.argv[2])
        print(m.dataFilter())

    if sys.argv[1] == "statistics":
        db.exportDBData(sys.argv[2])

    if sys.argv[1] == "histograms":
        db.histograms(sys.argv[2])

    if sys.argv[1] == "category-normalisation":
        db.normCategory('initial/LabeledDB/'+sys.argv[2],'initial', 5000, 100)
        db.viewCategory('initial/LabeledDB/'+sys.argv[2], debug=True)

    if sys.argv[1] == "view-category":
        db.viewCategory(os.path.realpath('output/LabeledDB/'+sys.argv[2]), absolutePath=True, debug=True)

if len(sys.argv) == 2:
    if sys.argv[1] == "full-normalisation":
        db.normalise(5000, 100)

    if sys.argv[1] == "view-category":
        for dir in os.scandir('output/LabeledDB'):
            if os.path.isdir(dir):
                db.viewCategory(os.path.realpath(dir), debug=True)