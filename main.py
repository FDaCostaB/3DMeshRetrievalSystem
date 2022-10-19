import sys
import DBData as db
from featureName import featureName, featureDimension
import os
from Features import FeaturesExtract
from Mesh import Mesh

def step3FullNormalization():
    db.normCategory('output/LabeledDB/Airplane')
    db.viewCategory('output/LabeledDB/Airplane', debug=True)
    # for dir in os.scandir('output/LabeledDB'):
    #    if os.path.isdir(dir):
    #        db.viewCategory(os.path.realpath(dir), debug=True)

def step2():
    db.normalise(5000, 100)
    db.extractData('initial')
    db.extractData('output')

if len(sys.argv) == 3:
    if sys.argv[1] == "analyze":
        m = Mesh(sys.argv[2])
        print(m.dataFilter())

    if sys.argv[1] == "statistics":
        db.exportDBData(sys.argv[2])

    if sys.argv[1] == "histograms":
        db.histograms(sys.argv[2])

    if sys.argv[1] == "full-normalisation":
        for dir in os.scandir('output/LabeledDB'):
            if os.path.isdir(dir):
                db.viewCategory(os.path.realpath(dir), debug=True)

    if sys.argv[1] == "category-normalisation":
        db.normCategory('initial/LabeledDB/'+sys.argv[2],'initial', 5000, 100)
        db.viewCategory('initial/LabeledDB/'+sys.argv[2], debug=True)