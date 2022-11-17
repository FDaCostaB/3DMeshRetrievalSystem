import sys
import DBData as db
import os
import LP as lp
from Mesh import Mesh
from Settings import readSettings, settings, settingsName
from tsne import tsne
import warnings

warnings.filterwarnings("ignore")
readSettings()

if len(sys.argv) == 3:
    if sys.argv[1] == "render":
        m = Mesh(sys.argv[2])
        m.render()

    if sys.argv[1] == "analyze":
        m = Mesh(sys.argv[2])
        print(m.dataFilter())

    if sys.argv[1] == "statistics":
        db.exportDBData(sys.argv[2]=="original")

    if sys.argv[1] == "histograms":
        db.histograms(sys.argv[2])

    if sys.argv[1] == "view-all-category":
        for dir in os.scandir(settings[settingsName.outputDBPath.value]):
            if os.path.isdir(dir):
                db.viewCategory(os.path.realpath(dir), sys.argv[2]=="original")

    if sys.argv[1] == "histogram-features":
        db.drawCategoryFeatures(sys.argv[2])

    # arg : emd or euclidean
    if sys.argv[1] == "distanceMatrix":
        db.exportDistanceMatrix(sys.argv[2])

    # arg : emd or euclidean
    # Set all weight to 1 before exportStats
    if sys.argv[1] == "exportStats":
        resAvg, resStd = db.exportStat(sys.argv[2])

    # exportStats before search for optimisedWeigth
    if sys.argv[1] == "optimisedWeigth":
        lp.ScalarOptimisedWeight()

    if sys.argv[1] == "tsne":
        distMatrix, rowLabel = db.parseDistMatrix(sys.argv[2])
        tsne(distMatrix, rowLabel, 100000)

if len(sys.argv) == 2:
    if sys.argv[1] == "full-normalisation":
        db.normalise()

    if sys.argv[1] == "features":
        db.exportDBFeatures()

    if sys.argv[1] == "lp":
        lp.ScalarOptimisedWeight()

    if sys.argv[1] == "evaluate":
        db.evaluateQuery()

    if sys.argv[1] == "time":
        db.timeQuery()

if len(sys.argv) == 4:
    if sys.argv[1] == "category-normalisation":
        db.normCategory(sys.argv[2])
        db.viewCategory(sys.argv[2], sys.argv[3]=="original")

    if sys.argv[1] == "view-category":
        db.viewCategory(sys.argv[2], sys.argv[3]=="original")

    if sys.argv[1] == "query":
        queryRes = db.query(sys.argv[2], "euclidean", k=int(sys.argv[3]))
        db.exportQueryRes(sys.argv[2], queryRes)

    if sys.argv[1] == "annQuery":
        tree, rowLabel = db.buildTree()
        queryTime = []
        queryRes = db.annQuery(sys.argv[2],sys.argv[3], tree, rowLabel)
        db.exportQueryRes(sys.argv[2], queryRes)

    if sys.argv[1] == "roc":
        db.ROC(sys.argv[2],sys.argv[3])