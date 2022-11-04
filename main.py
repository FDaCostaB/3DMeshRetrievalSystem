import sys
import DBData as db
import os
import LP as lp
from Mesh import Mesh
from Settings import readSettings, settings, settingsName
from tsne import tsne

readSettings()
files = ['output/NormaliseDB/Airplane/70.off',
'output/NormaliseDB/Ant/98.off',
'output/NormaliseDB/Armadillo/287.off',
'output/NormaliseDB/Bearing/348.off',
'output/NormaliseDB/Bird/256.off',
'output/NormaliseDB/Bust/304.off',
'output/NormaliseDB/Chair/114.off',
'output/NormaliseDB/Cup/37.off',
'output/NormaliseDB/Fish/223.off',
'output/NormaliseDB/FourLeg/381.off',
'output/NormaliseDB/Glasses/52.off',
'output/NormaliseDB/Hand/200.off',
'output/NormaliseDB/Human/10.off',
'output/NormaliseDB/Mech/328.off',
'output/NormaliseDB/Octopus/122.off',
'output/NormaliseDB/Plier/209.off',
'output/NormaliseDB/Table/150.off',
'output/NormaliseDB/Teddy/165.off',
'output/NormaliseDB/Vase/363.off']

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

if len(sys.argv) == 2:
    if sys.argv[1] == "full-normalisation":
        db.normalise()

    if sys.argv[1] == "features":
        db.exportDBFeatures()

    if sys.argv[1] == "query":
        resEucl = []
        resEmd = []
        for file in files:
            queryResEucl, queryResEMD = db.query(file, k=4)
            resEucl.append([file,queryResEucl])
            resEmd.append([file,queryResEMD])
        db.showQueriesRes(resEucl,"resEucl")
        db.showQueriesRes(resEmd,"resEMD")

    if sys.argv[1] == "tsne":
        distMatrix, rowLabel = db.parseDistMatrix("emd")
        tsne(distMatrix, rowLabel, 1000)

    if sys.argv[1] == "evaluate":
        db.evaluateQuery()


if len(sys.argv) == 4:
    if sys.argv[1] == "category-normalisation":
        db.normCategory(sys.argv[2])
        db.viewCategory(sys.argv[2], sys.argv[3]=="original")

    if sys.argv[1] == "view-category":
        db.viewCategory(sys.argv[2], sys.argv[3]=="original")

    if sys.argv[1] == "query":
        queryResEucl, queryResEMD = db.query(sys.argv[2], k=int(sys.argv[3]))
        db.exportQueryRes(sys.argv[2], queryResEucl)
        db.exportQueryRes(sys.argv[2], queryResEMD)

    if sys.argv[1] == "annQuery":
        queryRes = db.annQuery(sys.argv[2], k=int(sys.argv[3]))
        db.exportQueryRes(sys.argv[2], queryResEucl)