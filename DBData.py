import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import Math
from Features import FeaturesExtract, euclidianDist, emDist
from parse import getIndexList
from Mesh import Mesh
from dataName import dataName
from featureName import featureName, featureDimension
import pandas as pd
from Settings import settings,settingsName
from sklearn.neighbors import KDTree


# ---------------------------- STEP 2 ----------------------------------------#
def plotHistogram(df, feature, n_bins=20, size_x=10, size_y=7):
    if feature == dataName.PCA.value:
        parsedValues = []
        pca = []
        stringPCA = df[dataName.PCA.value].values
        for eigenvectors in stringPCA:
            parsedValues.append(eigenvectors.strip('][').split(', '))
        for vector in parsedValues:
            curr=[]
            vect=[]
            for coordinate in vector:
                if(coordinate[0]=='['):
                    coordinate = float(coordinate[1:])
                elif (coordinate[len(coordinate)-1] == ']'):
                    coordinate = float(coordinate[:-1])
                vect.append(float(coordinate))
                if(len(vect)==3):
                    curr.append(vect)
                    vect = []
                if(len(curr)==3):
                    pca.append(curr)
                    curr = []
        alignementVal = [[abs(Math.dotProduct(eigenvectors[0],[1,0,0])), abs(Math.dotProduct(eigenvectors[1],[0,1,0])),abs(Math.dotProduct(eigenvectors[2],[0,0,1]))] for eigenvectors in pca]
        XYZplotValue(alignementVal,feature)
    else:
        plotValue(df, feature, n_bins, size_x, size_y)


def histograms(feature):
    df = pd.read_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]),"statistics.csv"))
    outputDir = os.path.join(os.path.realpath(settings[settingsName.outputPath.value]),"histograms")
    os.makedirs(outputDir, exist_ok=True)
    plotHistogram(df, feature, 19)


def exportDBProp(fromOriginalDB):
    if fromOriginalDB:
        dbDir = os.path.realpath(settings[settingsName.dbPath.value])
    else :
        dbDir = os.path.realpath(settings[settingsName.outputDBPath.value])
    meshesData = []
    for dir in os.scandir(dbDir):
        if os.path.isdir(dir):
            FileIt = os.scandir(os.path.join(dbDir, dir.name))
            for file in FileIt:
                fileType = os.path.splitext(os.path.realpath(file))[1]
                if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                    mesh = Mesh(os.path.realpath(file))
                    data = mesh.dataFilter()
                    meshesData.append(data)
            FileIt.close()
    csvExport('statistics.csv', meshesData)
    return meshesData


def exportDBFeatures():
    normalisationType = settings[settingsName.normType.value]
    dbDir = os.path.realpath(settings[settingsName.outputDBPath.value])
    meshesData = []
    for dir in os.scandir(dbDir):
        if os.path.isdir(dir):
            FileIt = os.scandir(os.path.join(dbDir, dir.name))
            print(os.path.realpath(dir))
            for file in FileIt:
                fileType = os.path.splitext(os.path.realpath(file))[1]
                if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                    mesh = FeaturesExtract(os.path.realpath(file))
                    data = mesh.featureFilter()
                    meshesData.append(data)
            FileIt.close()
    if normalisationType == "Standardisation":
        meshesData = Math.standardisation(meshesData)
    elif normalisationType == "MinMax":
        meshesData = Math.minMaxNormalisation(meshesData)
    csvExport('features.csv', meshesData)
    return meshesData


def csvExport(fileName, data):
    filePath = os.path.join(os.path.realpath(settings[settingsName.outputPath.value]),fileName)
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    df = pd.DataFrame(data, columns=data[0].keys())
    df.to_csv(filePath,mode="w")


def normalise():
    dbDir = os.path.realpath(settings[settingsName.dbPath.value])
    for dir in os.scandir(dbDir):
        print(dir.name)
        normCategory(os.path.realpath(dir))


def plotValue(df, feature, n_bins=20, size_x=10, size_y=7):
    fig, axs = plt.subplots(1, 1, figsize=(size_x, size_y), tight_layout=True)
    plt.xlabel(feature)
    plt.ylabel("Number of mesh(es)")
    # if feature == dataName.SIDE_SIZE.value : n_bins = [0.99+i*0.001 for i in range(21)]
    # if feature == dataName.DIST_BARYCENTER.value : n_bins = [0+i*0.0001 for i in range(11)]
    # if feature == dataName.SIDE_SIZE.value : n_bins = [0+i*0.1 for i in range(21)]
    # if feature == dataName.FACE_NUMBERS.value : n_bins = [9000+i*100 for i in range(21)]
    # if feature == dataName.VERTEX_NUMBERS.value : n_bins = [4900+i*10 for i in range(21)]
    axs.hist(df[feature], bins=n_bins)
    plt.savefig(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]),"histograms", feature.lower() + settings[settingsName.imageExtension.value]))


def XYZplotValue(list, feature,size_x=10, size_y=7):
    fig, axs = plt.subplots(1,1,figsize=(size_x, size_y), tight_layout=True)
    data = [getIndexList(0, list), getIndexList(1, list), getIndexList(2, list)]
    colors = ['blue', 'red', 'yellow']
    labels = ['x', 'y', 'z']
    minVal = 0
    maxVal = max(data[0] + data[1] + data[2])
    Lbins = [minVal+i*((maxVal-minVal)/10) for i in range(11)]
    axs.hist(data, Lbins, histtype='bar', stacked=False, fill=True, label=labels, alpha=0.8, color=colors, edgecolor="k")
    plt.xticks(Lbins)
    plt.xlabel(feature)
    plt.ylabel('count')
    plt.legend()
    plt.savefig(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "histograms", feature.lower()+settings[settingsName.imageExtension.value]))


def normCategory(catName):
    path = os.path.join(os.path.realpath(settings[settingsName.dbPath.value]),catName)
    if os.path.isdir(path):
        FileIt = os.scandir(path)
        for file in FileIt:
            fileType = os.path.splitext(os.path.realpath(file))[1]
            if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                mesh = Mesh(os.path.realpath(file))
                mesh.resample()
                mesh.saveMesh()
        FileIt.close()


def viewCategory(catName, fromOriginalDB):
    debug = settings[settingsName.debug.value]
    totalMesh = 0
    if fromOriginalDB :
        outPath = os.path.join(settings[settingsName.dbPath.value], catName)
        path = os.path.join(settings[settingsName.dbPath.value], catName)
    else :
        outPath = os.path.join(settings[settingsName.outputDBPath.value], catName)
        path = os.path.join(settings[settingsName.outputDBPath.value], catName)
    os.makedirs(os.path.join(os.path.realpath(outPath),'screenshot'), exist_ok=True)
    if os.path.isdir(path):
        FileIt = os.scandir(path)
        for file in FileIt:
            fileType = os.path.splitext(os.path.realpath(file))[1]
            if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                totalMesh += 1
                mesh = Mesh(os.path.realpath(file))
                mesh.screenshot(os.path.join(os.path.realpath(outPath), 'screenshot'))
        FileIt.close()

    nbOfLine = (totalMesh//5)
    if totalMesh%5>0 : nbOfLine += 1
    fig, axs = plt.subplots(nbOfLine, 5, figsize=(30, 30))
    i=0
    if os.path.isdir(path):
        FileIt = os.scandir(os.path.join(os.path.realpath(outPath), 'screenshot'))
        for screen in FileIt:
            fileType = os.path.splitext(os.path.realpath(screen))[1]
            if screen.is_file() and fileType == ".jpg":
                image = mpimg.imread(os.path.realpath(screen))
                axs[i//5, i%5].imshow(image)
                axs[i//5, i%5].axis('off')
                i+=1
        FileIt.close()
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0, hspace=0.05)
    plt.savefig(outPath + "/meshes_overview"+ settings[settingsName.imageExtension.value])
    if(debug):
        plt.show()


# ---------------------------- STEP 3 ----------------------------------------#
def exportFeatures(funcName):
    dbDir = os.path.realpath(settings[settingsName.outputDBPath.value])
    dbHistValue = []
    dbScalarValue = []
    nbCat=0
    for dir in os.scandir(dbDir):
        if os.path.isdir(dir):
            catVal = getFeaturesHistogram(os.path.join(dbDir, dir.name), funcName)
            if featureDimension[funcName]==1:
                dbScalarValue.append(catVal)
            elif featureDimension[funcName]==2:
                dbHistValue.append(catVal)
            nbCat += 1
            print(dir.name)
    return dbScalarValue, dbHistValue, nbCat


def getFeaturesHistogram(path, funcName):
    FileIt = os.scandir(path)
    res = []
    if featureDimension[funcName] == 1:
        for file in FileIt:
            fileType = os.path.splitext(os.path.realpath(file))[1]
            if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                features = FeaturesExtract(os.path.realpath(file))
                featureVal = features.call(funcName)
                res.append(featureVal)
        FileIt.close()
        return [res, path]
    elif featureDimension[funcName] == 2:
        acc = []
        for file in FileIt:
            fileType = os.path.splitext(os.path.realpath(file))[1]
            if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                features = FeaturesExtract(os.path.realpath(file))
                featureVal = features.call(funcName)
                acc.append(featureVal)
        FileIt.close()
        return [acc, path]


def drawFeatures(funcName):
    print(funcName)
    dbScalarValue, dbHistValue, nbCat = exportFeatures(funcName)
    dbDir= settings[settingsName.outputDBPath.value]
    nbOfLine = (nbCat // 3)
    outputDir = os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "histograms")
    if nbCat % 3 > 0: nbOfLine += 1
    fig, axs = plt.subplots(nbOfLine, 3, figsize=(25, 35))

    if len(dbScalarValue) > 0:
        i=0
        for catValue in dbScalarValue:
            values = catValue[0]
            catName = catValue[1]
            if funcName == featureName.VOLUME.value: bins=[0.01*i for i in range(101)]
            elif funcName == featureName.SURFACE_AREA.value: bins=[0.1*i for i in range(51)]
            else: bins = 20
            axs[i//3, i%3].hist(values, bins=bins)
            axs[i//3, i%3].set_title(str(os.path.relpath(catName, dbDir)))
            i+=1
        while (i % 3) != 0:
            axs[i // 3, i % 3].set_visible(False)
            i+=1
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.3, hspace=0.4)
        plt.savefig(os.path.join(outputDir,funcName + settings[settingsName.imageExtension.value]))
        plt.cla()
        plt.clf()

    if len(dbHistValue) > 0:
        i = 0
        for catValue in dbHistValue:
            values = catValue[0]
            catName = catValue[1]
            for objvalue in values:
                axs[i // 3, i % 3].plot(objvalue[0], objvalue[1])
            axs[i // 3, i % 3].set_title(str(os.path.relpath(catName, dbDir)))
            i += 1
        while (i % 3) != 0:
            axs[i // 3, i % 3].set_visible(False)
            i += 1
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.3)
        plt.savefig(os.path.join(outputDir, funcName + settings[settingsName.imageExtension.value]))


def drawCategoryFeatures(functionName):
    if functionName == "all":
        functionsName = [f.value for f in featureName if f != featureName.FILENAME and f != featureName.DIRNAME]
    elif functionName == "histogram":
        functionsName = [featureName.A3.value, featureName.D1.value , featureName.D2.value, featureName.D3.value, featureName.D4.value]
    elif functionName == "scalar":
        functionsName = [featureName.SURFACE_AREA.value, featureName.VOLUME.value , featureName.COMPACTNESS.value,
                         featureName.SPHERICITY.value, featureName.RECTANGULARITY.value, featureName.DIAMETER.value,
                         featureName.ECCENTRICITY.value, featureName.CENTROID.value]
    else:
        functionsName = [functionName]
    for funcName in functionsName:
        drawFeatures(funcName)

# ---------------------------- STEP 3 ----------------------------------------#
def parseFeatures():
    df = pd.read_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "features.csv"))
    DB = []
    line = {}
    avg = {}
    std = {}
    min = {}
    max = {}

    for i, row in df.iterrows():
        for colName in df.columns:
            if colName[:7]!='Unnamed' and row['File name'] not in ['avg', 'std']:
                line[colName] = row[colName]
            elif row['File name'] == 'avg':
                for colName in df.columns:
                    if colName[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and colName != 'Unnamed: 0':
                        avg[colName] = row[colName]
            elif row['File name'] == 'std':
                for colName in df.columns:
                    if colName[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and colName != 'Unnamed: 0':
                        std[colName] = row[colName]
            elif row['File name'] == 'min':
                for colName in df.columns:
                    if colName[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and colName != 'Unnamed: 0':
                        min[colName] = row[colName]
            elif row['File name'] == 'max':
                for colName in df.columns:
                    if colName[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and colName != 'Unnamed: 0':
                        max[colName] = row[colName]
        if len(line)>0: DB.append(line)
        line = {}
    if len(avg) > 0 and len(std) > 0 :
        return DB, avg, std, "Standardisation"
    elif len(min) > 0 and len(max) > 0 :
        return DB, min, max, "MinMax"


def exportDistanceMatrix(distanceFunc):
    DB, norm1, norm2, normalisationType = parseFeatures()
    res = []
    i =0
    for obj1 in DB:
        row = {}
        row['OBJ1']=obj1["Folder name"]+'/'+obj1["File name"]
        for obj2 in DB:
            if obj1["File name"] not in ["avg","std","min","max"] and obj2["File name"] not in ["avg","std","min","max"]:
                if distanceFunc.lower()=="emd":
                    row[obj2["Folder name"]+'/'+obj2["File name"]] = emDist(obj1,obj2)[0]
                elif distanceFunc.lower()=="euclidean":
                    row[obj2["Folder name"]+'/'+obj2["File name"]] = euclidianDist(obj1, obj2)[0]
        res.append(row)
        i+=1
        if i%20==0 : print(str(int(i/380*100))+" %")
    if distanceFunc.lower() == "emd":
        csvExport('distanceEMD.csv', res)
    elif distanceFunc.lower() == "euclidean":
        csvExport('distanceEucl.csv', res)
    return res


def parseDistMatrix(distanceFunc):
    if distanceFunc.lower() == "emd":
        df = pd.read_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "distanceEMD.csv"))
    elif distanceFunc.lower() == "euclidean":
        df = pd.read_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "distanceEucl.csv"))
    else:
        return
    rowLabel = []
    distMatrix = np.zeros((df.shape[0],df.shape[0]))
    for i, row in df.iterrows():
        j = 0
        rowLabel.append(row['OBJ1'].split('/')[0])
        for colName in df.columns:
            if colName[:7]!='Unnamed' and colName != 'OBJ1':
                distMatrix[i][j] = row[colName]
                j+=1
    return distMatrix, rowLabel


def exportFeaturesDist(distanceFunc):
    DB, norm1, norm2, normalisationType = parseFeatures()
    categories = list(set([obj['Folder name'] for obj in DB]))
    categories.sort()
    pairDist = {}

    i =0
    for obj1 in DB:
        for obj2 in DB:
            if obj1["File name"] not in ["avg","std","min","max"] and obj2["File name"] not in ["avg","std","min","max"] and obj1["Folder name"] >= obj2["Folder name"]:
                if distanceFunc.lower()=="emd":
                    if (obj1["Folder name"]+"-"+obj2["Folder name"]) not in pairDist.keys() :
                        pairDist[obj1["Folder name"] + "-" + obj2["Folder name"]] = []
                    pairDist[obj1["Folder name"] + "-" + obj2["Folder name"]].append(emDist(obj1, obj2)[3])
                elif distanceFunc.lower()=="euclidean":
                    if (obj1["Folder name"] + "-" + obj2["Folder name"]) not in pairDist.keys() :
                        pairDist[obj1["Folder name"] + "-" + obj2["Folder name"]] = []
                    pairDist[obj1["Folder name"] + "-" + obj2["Folder name"]].append(euclidianDist(obj1, obj2)[3])
        i+=1
        if i%20==0 : print(str(int(i/380*100))+" %")

    resAvg = []
    for pairKey in pairDist.keys():
        avg = {}
        avg['Pair'] = pairKey
        for feature in featureName:
            if feature.value not in ['Folder name', 'File name']:
                distPairFeat = np.array([distList[feature.value] for distList in pairDist[pairKey]])
                avg[feature.value]= distPairFeat.mean()
        resAvg.append(avg)
    csvExport("catAvg.csv",resAvg)
    return resAvg

# ---------------------------- STEP 4/5 ----------------------------------------#
def buildTree():
    DB, norm1, norm2, normalisationType = parseFeatures()

    if len(DB)>0:
        featMat = np.zeros((len(DB), len(DB[0])-2))
    else :
        return
    colLabel = []
    rowLabel = []
    i = 0
    for row in DB:
        rowLabel.append(os.path.join(row[featureName.DIRNAME.value],row[featureName.FILENAME.value]))
        j=0
        for key in row.keys():
                if key not in [featureName.DIRNAME.value,featureName.FILENAME.value]:
                    if i == 0:
                        colLabel.append(key)
                    featMat[i][j]=row[key]
                    j+=1
        i+=1
    tree = KDTree(featMat, leaf_size=4)
    return tree, rowLabel



def annQuery(path, k, tree, rowLabel):
    mesh = Mesh(os.path.realpath(path))
    mesh.resample()
    mesh.saveMesh(os.path.join(settings[settingsName.outputPath.value], "normaliseQueriedMesh"))
    mesh = FeaturesExtract(os.path.join(settings[settingsName.outputPath.value],
                                        "normaliseQueriedMesh" + settings[settingsName.meshExtension.value]))
    queryFeatures = mesh.featureFilter(10000)
    queryFeatures[featureName.FILENAME.value] = os.path.basename(path)

    dd, ii = tree.query([[queryFeatures[key] for key in queryFeatures.keys() if key not in [featureName.DIRNAME.value, featureName.FILENAME.value]]], k=k)
    return [(rowLabel[index], 0, []) for index in ii[0]]


def query(path, qtype, tree=None, rowLabel=None, k=5):
    if qtype == "ann":
        return annQuery(path, k, tree, rowLabel)
    mesh = Mesh(os.path.realpath(path))
    mesh.resample()
    mesh.saveMesh(os.path.join(settings[settingsName.outputPath.value],"normaliseQueriedMesh"))
    mesh = FeaturesExtract(os.path.join(settings[settingsName.outputPath.value],"normaliseQueriedMesh"+settings[settingsName.meshExtension.value]))

    queryFeatures = mesh.featureFilter(10000)
    queryFeatures[featureName.FILENAME.value] = os.path.basename(path)
    DB, norm1, norm2, normalisationType = parseFeatures()

    for key in queryFeatures.keys():
        if key[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and key not in ['File name', 'Folder name']:
            if normalisationType == "Standardisation":
                avg=norm1
                std=norm2
                queryFeatures[key] = (queryFeatures[key] - avg[key]) / std[key]
            elif normalisationType == "MinMax":
                min = norm1
                max = norm2
                queryFeatures[key] = (queryFeatures[key] - min[key]) / (max[key]-min[key])

    distListEucl = []
    distListEMD = []
    for row in DB:
        if row["File name"] not in ["avg","std","min","max"]:
            if qtype.lower() == "euclidean" :
                distListEucl.append(euclidianDist(queryFeatures, row))
            elif qtype.lower() == "emd" :
                distListEMD.append(emDist(queryFeatures, row))
    if qtype.lower() == "euclidean":
        distListEucl.sort(key=lambda val: val[0])
    elif qtype.lower() == "emd":
        distListEMD.sort(key=lambda val: val[0])
    if qtype.lower() == "euclidean":
        return [(os.path.relpath(p2,'.'), dist, dContrib) for dist, p1, p2, dContrib in distListEucl[:k]]
    elif qtype.lower() == "emd":
        return [(os.path.relpath(p2,'.'), dist, dContrib) for dist, p1, p2,dContrib in distListEMD[:k]]


def saveQueryRes(queryShape, res):
    os.makedirs(os.path.join(os.path.realpath('output'), 'screenshot'), exist_ok=True)
    mesh = Mesh(os.path.realpath(os.path.relpath(queryShape, '.')))
    mesh.screenshot(os.path.join(os.path.realpath('output'), 'screenshot'), fileName='query')
    i = 0
    results = {}
    for path,dist,dContrib in res:
        mesh = Mesh(os.path.join(os.path.realpath(settings[settingsName.outputDBPath.value]), path))
        mesh.screenshot(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'), fileName=str(i))
        results[str(i)] = str("%.4f" % dist)
        i += 1
    return results


def exportQueryRes(queryShape, res):
    fig, axs = plt.subplots(1, 5, figsize=(18, 4))
    i = 1

    os.makedirs(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'), exist_ok=True)
    mesh = Mesh(os.path.realpath(queryShape))
    mesh.screenshot(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'),fileName='res0')
    for path,dist,dcontrib in res[:4]:
        mesh = Mesh(os.path.join(os.path.realpath(settings[settingsName.outputDBPath.value]),path))
        mesh.screenshot(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'), fileName='res'+str(i))
        i += 1

    parDir = os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot')
    screen = os.path.join(os.path.realpath(parDir), 'res0.jpg')
    image = mpimg.imread(os.path.realpath(screen))
    axs[0].set_title('Query shape')
    axs[0].imshow(image)
    for i in range(1,5):
        screen = os.path.join(os.path.realpath(parDir), 'res'+str(i)+'.jpg')
        fileType = os.path.splitext(os.path.realpath(screen))[1]
        if os.path.isfile(screen) and fileType == ".jpg":
            image = mpimg.imread(os.path.realpath(screen))
            axs[i%5].set_title(res[i-1][0] +'\n d='+str(res[i-1][1]))
            axs[i%5].imshow(image)
            i += 1
    for i in range(5):
        axs[i].axis('off')
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.5, hspace=0.05)
    plt.show()

# ---------------------------- STEP 6 ----------------------------------------#
def evaluateQuery():
    df = pd.read_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "features.csv"))
    counter = 0
    evalResEMD = []
    evalResEucl = []
    for i, row in df.iterrows():
        if row["File name"] not in ["avg", "std"]:
            queryPath = os.path.join(os.path.realpath(settings[settingsName.outputDBPath.value]),row["Folder name"],row["File name"])
            queryResEucl = query(queryPath, "euclidean", 380)
            queryResEMD = query(queryPath, "emd", 380)

            for dType in ["emd","euclidean"]:
                if dType.lower() == "emd":
                    queryRes = queryResEMD[:20]
                elif dType.lower() == "euclidean":
                    queryRes = queryResEucl[:20]

                tP = 0
                fP = 0
                for q in queryRes:
                    rPath = q[0]
                    rClass = rPath.split("\\")[0]
                    if rClass == row["Folder name"]:
                        tP += 1
                    else:
                        fP += 1
                fN = 20 - tP
                tN = 360 - fP
                rowRes = {
                    "fileName": row["File name"],
                    "className": row["Folder name"],
                    "TP": tP,
                    "FP": fP,
                    "TN": tN,
                    "FN": fN,
                    "Total Performance": (fP + fN) / 380,
                    "Accuracy" : (tP+tN) / 380,
                    "Precision" : tP /(tP+fP),
                    "Recall/Sensitivity" : tP /(tP+fN),
                    "Specificity": tN / (fP + tN)
                }

                if dType.lower() == "emd":
                    queryRes = queryResEMD
                elif dType.lower() == "euclidean":
                    queryRes = queryResEucl

                roc = []
                for k in range(1,381):
                    querySize = queryRes[:k]
                    tP = 0
                    fP = 0
                    for q in querySize:
                        rPath = q[0]
                        rClass = rPath.split("\\")[0]
                        if rClass == row["Folder name"]:
                            tP += 1
                        else:
                            fP += 1
                    fN = 20 - tP
                    tN = 380 - fP
                    Sensitivity = tP / (tP + fN)
                    Specificity = tN / (fP + tN)
                    roc.append([Sensitivity,Specificity])
                auroc = sum([val[0] for val in roc])/len(roc)
                rowRes["AUROC"] = auroc
                if dType.lower() == "emd":
                    evalResEMD.append(rowRes)
                elif dType.lower() == "euclidean":
                    evalResEucl.append(rowRes)

                counter += 1
                if counter % 40 == 0: print(str(int(counter / 760 * 100)) + " %")

    rDF = pd.DataFrame(evalResEMD)
    rDF.to_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "evaluation-emd.csv"))
    rDF = pd.DataFrame(evalResEucl)
    rDF.to_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "evaluation-eucl.csv"))


def timeQuery(distanceFunc):
    import time
    tree, rowLabel = buildTree()

    df = pd.read_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), "features.csv"))
    queryTime = []
    for i, row in df.iterrows():
        if row["File name"] not in ["avg", "std"]:
            queryPath = os.path.join(os.path.realpath(settings[settingsName.outputDBPath.value]),row["Folder name"],row["File name"])
            start = time.time()
            query(queryPath, distanceFunc, tree, rowLabel, 20)
            end = time.time()
            queryTime.append((end - start) * 10 ** 3)
            print(i)
            print((end - start) * 10 ** 3)
    time = np.array(queryTime)
    print("Mean : ")
    print(time.mean())
    print("Std : ")
    print(time.std())
    print("Median : ")
    print(np.median(time))
    print("Max : ")
    print(time.max())
    print("Min : ")
    print(time.min())