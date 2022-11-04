import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import bisect
import Math
from Features import FeaturesExtract, euclidianDist, emDist
from parse import getIndexList
from Mesh import Mesh
from dataName import dataName
from featureName import featureName, featureDimension
import pandas as pd
from Settings import settings,settingsName


# ---------------------------- STEP 2 ----------------------------------------#
def plotHistogram(df, feature, n_bins=20, size_x=10, size_y=7):
    outputDir = os.path.join(os.path.realpath(settings[settingsName.outputPath.value]),"histograms")
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
        XYZplotValue(alignementVal,feature,outputDir)
    else:
        plotValue(df, feature, outputDir, n_bins, size_x, size_y)


def histograms(feature):
    df = pd.read_csv(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]),"statistics.csv"))
    outputDir = os.path.join(os.path.realpath(settings[settingsName.outputPath.value]),"histograms")
    os.makedirs(outputDir, exist_ok=True)
    plotHistogram(df, feature, 19)


def exportDBData(fromOriginalDB):
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
        print(normalisationType)
        meshesData = Math.standardisation(meshesData)
    elif normalisationType == "MinMax":
        print(normalisationType)
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


def plotValue(df, feature, outputDir, n_bins=20, size_x=10, size_y=7):
    fig, axs = plt.subplots(1, 1, figsize=(size_x, size_y), tight_layout=True)
    plt.xlabel(feature)
    plt.ylabel("Number of mesh(es)")
    if feature == dataName.SIDE_SIZE.value and outputDir==os.path.realpath('output/histograms'): n_bins = [0.99+i*0.001 for i in range(21)]
    if feature == dataName.DIST_BARYCENTER.value and outputDir==os.path.realpath('output/histograms'): n_bins = [0+i*0.0001 for i in range(11)]
    if feature == dataName.SIDE_SIZE.value and outputDir==os.path.realpath('output/histograms'): n_bins = [0+i*0.1 for i in range(21)]
    if feature == dataName.FACE_NUMBERS.value and outputDir==os.path.realpath('output/histograms'): n_bins = [9000+i*100 for i in range(21)]
    if feature == dataName.VERTEX_NUMBERS.value and outputDir==os.path.realpath('output/histograms'): n_bins = [4900+i*10 for i in range(21)]
    axs.hist(df[feature], bins=n_bins)
    plt.savefig(outputDir+ "\\" +feature.lower()+".png")


def XYZplotValue(list, feature, outputDir,size_x=10, size_y=7):
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
    plt.savefig(outputDir+ "\\" +feature.lower()+".png")


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
    plt.savefig(outPath + "/meshes_overview.jpg")
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
            catVal=getFeaturesHistogram(os.path.join(dbDir, dir.name), funcName)
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
        plt.savefig(os.path.join(outputDir,funcName + ".jpg"))
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
        plt.savefig("./output/" + funcName + ".jpg")


def drawCategoryFeatures(functionsName):
    if functionsName == "all":
        functionsName = [f.value for f in featureName]
    elif functionsName == "histogram":
        functionsName = [featureName.A3.value, featureName.D1.value , featureName.D2.value, featureName.D3.value, featureName.D4.value]
    elif functionsName == "scalar":
        functionsName = [featureName.SURFACE_AREA.value, featureName.VOLUME.value , featureName.COMPACTNESS.value,
                         featureName.SPHERICITY.value, featureName.RECTANGULARITY.value, featureName.DIAMETER.value,
                         featureName.ECCENTRICITY.value, featureName.CENTROID.value]
    else:
        functionsName = [functionsName]
    for funcName in functionsName:
        drawFeatures(funcName)


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
        row['OBJ1']=obj1["File name"]
        for obj2 in DB:
            if obj1["File name"] not in ["avg","std","min","max"] and obj2["File name"] not in ["avg","std","min","max"]:
                if distanceFunc.lower()=="emd":
                    row[obj2["File name"]] = emDist(obj1,obj2)[0]
                elif distanceFunc.lower()=="euclidean":
                    row[obj2["File name"]] = euclidianDist(obj1, obj2)[0]
        res.append(row)
        i+=1
        if i%20==0 : print(str(int(i/380*100))+" %")
    if distanceFunc.lower() == "emd":
        csvExport('distanceEMD.csv', res)
    elif distanceFunc.lower() == "euclidean":
        csvExport('distanceEucl.csv', res)
    return res

def exportStat(distanceFunc):
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
    resStd = []
    for pairKey in pairDist.keys():
        avg = {}
        std = {}
        avg['Pair'] = pairKey
        std['Pair'] = pairKey
        for feature in featureName:
            if feature.value not in ['Folder name', 'File name']:
                distPairFeat = np.array([distList[feature.value] for distList in pairDist[pairKey]])
                avg[feature.value]= distPairFeat.mean()
                std[feature.value]= distPairFeat.mean()
        resAvg.append(avg)
        resStd.append(std)

    csvExport("catAvg.csv",resAvg)
    csvExport("catStd.csv",resStd)
    return resAvg, resStd


def query(path, k=5):
    mesh = Mesh(os.path.realpath(path))
    mesh.resample()
    mesh.saveMesh(os.path.join(settings[settingsName.outputPath.value],"normaliseQueriedMesh"))
    mesh = FeaturesExtract(os.path.join(settings[settingsName.outputPath.value],"normaliseQueriedMesh."+settings[settingsName.meshExtension.value]))

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
        if row["File name"]!=queryFeatures["File name"] and row["File name"] not in ["avg","std","min","max"]:
            bisect.insort(distListEucl, euclidianDist(queryFeatures,row))
            bisect.insort(distListEMD, emDist(queryFeatures,row))
    return [(os.path.relpath(p2,'.'), dist, dContrib) for dist, p1, p2, dContrib in distListEucl[:k]], [(os.path.relpath(p2,'.'), dist, dContrib) for dist, p1, p2,dContrib in distListEMD[:k]]

def displayQueryRes(queryShape, res):
    nbOfLine = (len(res) // 5)
    if len(res) % 5 > 0: nbOfLine += 1
    fig, axs = plt.subplots(nbOfLine+1, 5, figsize=(18, 4*nbOfLine))
    i = 1
    os.makedirs(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'), exist_ok=True)
    mesh = Mesh(os.path.realpath(queryShape))
    mesh.screenshot(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'),fileName='res0')
    for path,dist in res:
        mesh = Mesh(os.path.join(os.path.realpath(settings[settingsName.outputDBPath.value]),path))
        mesh.screenshot(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'), fileName='res'+str(i))
        i += 1

    parDir = os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot')
    screen = os.path.join(os.path.realpath(parDir), 'res0.jpg')
    image = mpimg.imread(os.path.realpath(screen))
    axs[0, 2].set_title('Query shape')
    axs[0, 2].imshow(image)
    for i in range(1,len(res)+1):
        screen = os.path.join(os.path.realpath(parDir), 'res'+str(i)+'.jpg')
        fileType = os.path.splitext(os.path.realpath(screen))[1]
        if os.path.isfile(screen) and fileType == ".jpg":
            image = mpimg.imread(os.path.realpath(screen))
            axs[(i-1)//5+1, (i-1)%5].set_title(res[i-1][0] +'\n d='+str(res[i-1][1]))
            axs[(i-1)//5+1, (i-1)%5].imshow(image)
            i += 1
    for i in range(len(res)+5):
        axs[i // 5, i % 5].axis('off')
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.5, hspace=0.05)
    plt.show()


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

def showQueriesRes(queries,resfile):
    fig, axs = plt.subplots(len(queries), 5, figsize=(18, 5*len(queries)))
    filePos = []

    os.makedirs(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'), exist_ok=True)
    i = 0
    for query in queries:
        mesh = Mesh(os.path.realpath(query[0]))
        mesh.screenshot(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'),fileName='query'+str(i))
        filePos.append([i,os.path.join(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'),'query'+str(i)+'.jpg')])
        j = 1
        for res in query[1]:
            mesh = Mesh(os.path.join(os.path.realpath(settings[settingsName.outputDBPath.value]),res[0]))
            mesh.screenshot(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'), fileName='res'+str(j+i))
            filePos.append([j+i, os.path.join(os.path.join(os.path.realpath(settings[settingsName.outputPath.value]), 'screenshot'),'res' + str(j+i)+'.jpg')])
            j += 1
        i += 5

    filePos.sort()
    for elem in filePos:
        image = mpimg.imread(os.path.realpath(elem[1]))
        axs[elem[0]//5, elem[0] % 5].imshow(image)
        axs[elem[0] // 5, elem[0] % 5].axis("off")
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.5, hspace=0.05)
    plt.savefig(settings[settingsName.outputPath.value]+ "\\"+resfile+".png")