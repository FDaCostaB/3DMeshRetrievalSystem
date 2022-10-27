import sys
import DBData as db
import os
from Mesh import Mesh
from Settings import readSettings, settings, settingsName

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

if len(sys.argv) == 2:
    if sys.argv[1] == "full-normalisation":
        db.normalise()

    if sys.argv[1] == "features":
        db.exportDBFeatures()

if len(sys.argv) == 4:
    if sys.argv[1] == "category-normalisation":
        db.normCategory(sys.argv[2])
        db.viewCategory(sys.argv[2], sys.argv[3]=="original")

    if sys.argv[1] == "view-category":
        db.viewCategory(sys.argv[2], sys.argv[3]=="original")

    if sys.argv[1] == "query":
        queryResEucl, queryResEMD = db.query(sys.argv[2], k=int(sys.argv[3]))
        db.displayQueryRes(sys.argv[2], queryResEucl)
        db.displayQueryRes(sys.argv[2], queryResEMD)