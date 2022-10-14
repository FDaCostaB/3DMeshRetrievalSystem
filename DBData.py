import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Features import FeaturesExtract
from parse import getFieldList, getIndexList
from Mesh import Mesh
from dataName import dataName, dataDimension
from featureName import featureName, featureDimension
from DebugLog import debugLvl, debugLog
import numpy as np



def plot(outputDir, dictList, featuresList, n_bins=20, size_x=10, size_y=7):
    for feature in featuresList:
        dataVisualisation(getFieldList(feature, dictList), feature, outputDir, n_bins, size_x, size_y)

def plot3D(outputDir, dictList, featuresList):
    for feature in featuresList:
        if dataName.PCA.value == feature:
            mainComponentPCA = getIndexList(0, getFieldList(feature, dictList))
            XYZdataVisualisation(mainComponentPCA, feature, outputDir)
        else :
            XYZdataVisualisation(getFieldList(feature, dictList), feature, outputDir)

def histograms(outputDir, features):
    dictList = exportDBData()
    if dataName.CATEGORY in features :
        plot([dataName.CATEGORY.value], 26, 25, 10)
    oneD = [f.value for f in features if dataDimension[f] == 1 and f != dataName.CATEGORY]
    threeD = [f.value for f in features if dataDimension[f] == 3]
    if len(threeD) != 0: plot3D(outputDir, dictList, threeD)
    if len(oneD) != 0: plot(outputDir, dictList, oneD)

def exportDBData(outputDir):
    dirs = [
        "./"+outputDir+"/PRINCETON",
        "./"+outputDir+"/LabeledDB"
    ]
    acc = []
    for dir in dirs:
        acc += exportDirData(dir)
    return acc
def exportDirData(dbDir):
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
    csvExport('data'+dbDir+'.csv', meshesData)
    return meshesData

def csvExport(outputDir, fileName, data):
    filePath = os.path.join(os.path.realpath("./"+outputDir),fileName)
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    file = open(filePath, "w")
    csvDictWriter = csv.DictWriter(file, fieldnames=data[0].keys())
    csvDictWriter.writeheader()
    csvDictWriter.writerows(data)


def normalization():
    dirs = [
        "./remesh/PRINCETON",
        "./remesh/LabeledDB"
    ]
    for dir in dirs:
        normalise(dir)

def normalise(dbDir):
    for dir in os.scandir(dbDir):
        if os.path.isdir(dir):
            FileIt = os.scandir(os.path.join(dbDir, dir.name))
            for file in FileIt:
                fileType = os.path.splitext(os.path.realpath(file))[1]
                if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                    mesh = Mesh(os.path.realpath(file))
                    mesh.resample()
                    mesh.saveMesh()
            FileIt.close()

def dataVisualisation(list, feature, outputDir, n_bins=20, size_x=10, size_y=7):
    fig, axs = plt.subplots(1, 1, figsize=(size_x, size_y), tight_layout=True)

    plt.xlabel(feature)
    plt.ylabel("Number of mesh(es)")
    if(feature == dataName.SIDE_SIZE.value and outputDir=='output') : n_bins = [0.99+i*0.001 for i in range(21)]
    if(feature == dataName.DIST_BARYCENTER.value and outputDir=='output') : n_bins = [0+i*0.0001 for i in range(11)]
    if(feature == dataName.SIDE_SIZE.value and outputDir=='remesh') :n_bins = [0+i*0.1 for i in range(21)]
    axs.hist(list, bins=n_bins)
    plt.savefig("./" + outputDir + "/" + feature.lower() + '.png')


def XYZdataVisualisation(list, feature, outputDir,size_x=10, size_y=7):
    fig, axs = plt.subplots(1,1,figsize=(size_x, size_y), tight_layout=True)
    data = [getIndexList(0, list, feature == dataName.PCA.value), getIndexList(1, list, feature == dataName.PCA.value), getIndexList(2, list, feature == dataName.PCA.value)]
    colors = ['blue', 'red', 'yellow']
    labels = ['x', 'y', 'z']
    minVal = min(data[0] + data[1] + data[2])
    maxVal = max(data[0] + data[1] + data[2])
    Lbins = [minVal+i*((maxVal-minVal)/10) for i in range(11)]
    axs.hist(data, Lbins, histtype='bar', stacked=False, fill=True, label=labels, alpha=0.8, color=colors, edgecolor="k")
    plt.xticks(Lbins)
    plt.xlabel(feature)
    plt.ylabel('count')
    plt.legend()
    plt.savefig("./" + outputDir + "/" + feature.lower() + '.png')


def exportFeatures(dbDir, funcName):
    dbHistValue = []
    dbScalarValue = []
    nbCat=0
    for dir in os.scandir(dbDir):
        if os.path.isdir(dir):
            catVal=drawHistogram(os.path.join(dbDir, dir.name),funcName)
            if featureDimension[funcName]==1: dbScalarValue.append(catVal)
            elif featureDimension[funcName]==2: dbHistValue.append(catVal)
            nbCat += 1
    return dbScalarValue, dbHistValue, nbCat


def drawHistogram(path, funcName):
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
        for objVal in acc:
            y, binEdges = np.histogram(objVal, bins=50)
            x = 0.5 * (binEdges[1:] + binEdges[:-1])
            res.append([x, y])
        return [res,path]


def drawFeatures(dbDir, funcName):
    dbScalarValue, dbHistValue, nbCat = exportFeatures(dbDir, funcName)

    nbOfLine = (nbCat // 3)
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
        plt.savefig("./output/" + funcName + ".jpg")

    if len(dbHistValue) > 0:
        plt.cla()
        plt.clf()
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

def drawCategoryFeatures(dbDir,functionsName=None):
    if functionsName is None: functionsName = [f.value for f in featureName]
    for funcName in functionsName:
        drawFeatures(dbDir, funcName)

def normCategory(path):
    totalMesh = 0
    if os.path.isdir(path):
        FileIt = os.scandir(path)
        for file in FileIt:
            fileType = os.path.splitext(os.path.realpath(file))[1]
            if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                totalMesh += 1
                mesh = Mesh(os.path.realpath(file))
                mesh.normalise()
                mesh.saveMesh()
        FileIt.close()


def viewCategory(path, camPos="diagonal", absolutePath=False, debug=False):
    totalMesh = 0
    if absolutePath :
        outPath = path
    else :
        outPath = os.path.join('./output', os.path.relpath(path, './remesh'))
    os.makedirs(os.path.join(os.path.realpath(outPath),'screenshot'), exist_ok=True)
    if os.path.isdir(path):
        FileIt = os.scandir(outPath)
        for file in FileIt:
            fileType = os.path.splitext(os.path.realpath(file))[1]
            if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                totalMesh += 1
                mesh = Mesh(os.path.realpath(file))
                mesh.screenshot(os.path.join(os.path.realpath(outPath), 'screenshot'), camPos)
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
                # axs[i//5, i%5].set_title(str(screen.name))
                i+=1
        FileIt.close()
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0, hspace=0.05)
    plt.savefig(outPath + "/meshes_overview.jpg")
    if(debug):
        plt.show()


def plot(folder):
    histograms(folder, [dataName.VERTEX_NUMBERS, dataName.SIDE_SIZE, dataName.DIST_BARYCENTER])