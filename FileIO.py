import csv
import os
from Mesh import Mesh
from dataName import dataName, dataDimension
import matplotlib.pyplot as plt
from Debug import debugLvl,debugLog

class DataIO:
    def __init__(self,outputDir):
        self.pctPath = "./"+outputDir+"/PRINCETON/test"
        self.lblPath = "./"+outputDir+"/LabeledDB_new"
        self.outputDir = outputDir
        self.dictList = []

    def exportMeshesData(self):
        meshesData1 = []
        for dir in os.scandir(self.lblPath):
            FileIt =os.scandir(os.path.join(self.lblPath, dir.name))
            for file in FileIt:
                fileType = os.path.splitext(os.path.realpath(file))[1]
                if fileType == ".obj" or fileType == ".off":
                    mesh = Mesh(os.path.realpath(file))
                    data = mesh.dataFilter()
                    if data is not None : meshesData1.append(data)
                    mainComponentPCA = getIndexList(0, data[dataName.PCA.value])
                    if abs(float(mainComponentPCA[0])) < 0.8:
                        debugLog(os.path.realpath(file),debugLvl.WARNING)
                        debugLog(str(mainComponentPCA),debugLvl.WARNING)
            FileIt.close()
        self.writeData('dataLabeledDB.csv',meshesData1)

        meshesData2 = []
        for dir in os.scandir(self.pctPath):
            FileIt =os.scandir(os.path.join(self.pctPath, dir.name))
            for file in FileIt:
                fileType = os.path.splitext(os.path.realpath(file))[1]
                if fileType == ".obj" or fileType == ".off":
                    mesh = Mesh(os.path.realpath(file))
                    data = mesh.dataFilter()
                    if data is not None : meshesData2.append(data)
            FileIt.close()
        self.writeData('dataPriceton.csv',meshesData2)
        self.dictList = meshesData1 + meshesData2

    def writeData(self,fileName,data):
        filePath = os.path.join(os.path.realpath("./"+self.outputDir),fileName)
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        file = open(filePath, "w")
        csvDictWriter = csv.DictWriter(file, fieldnames=data[0].keys())
        csvDictWriter.writeheader()
        csvDictWriter.writerows(data)

    def plotFeatures(self, featuresList, n_bins=20, size_x=10, size_y=7):
        for feature in featuresList:
            dataVisualisation(getFieldList(feature, self.dictList), feature, self.outputDir, n_bins, size_x, size_y)

    def plot3DFeatures(self, featuresList):
        for feature in featuresList:
            if dataName.PCA.value == feature:
                mainComponentPCA = getIndexList(0, getFieldList(feature, self.dictList))
                XYZdataVisualisation(mainComponentPCA, feature, self.outputDir)
            else :
                XYZdataVisualisation(getFieldList(feature, self.dictList), feature, self.outputDir)

    def plotHistograms(self,features):
        self.exportMeshesData()
        if dataName.CATEGORY in features :
            self.plotFeatures([dataName.CATEGORY.value], 26, 25, 10)
        OneD = [f.value for f in features if dataDimension[f] == 1 and f != dataName.CATEGORY]
        ThreeD = [f.value for f in features if dataDimension[f] == 3]
        self.plot3DFeatures(ThreeD)
        self.plotFeatures(OneD)


def normaliseDB(expectedVerts,eps):
    totalMesh = 0
    for dir in os.scandir("./Models/PRINCETON/test"):
        FileIt = os.scandir(os.path.join("./Models/PRINCETON/test", dir.name))
        for file in FileIt:
            fileType = os.path.splitext(os.path.realpath(file))[1]
            if fileType == ".obj" or fileType == ".off":
                totalMesh += 1
                mesh = Mesh(os.path.realpath(file))
                mesh.resample(expectedVerts, eps)
                mesh.saveMesh()
        FileIt.close()
    for dir in os.scandir("./Models/LabeledDB_new"):
        FileIt =os.scandir(os.path.join("./Models/LabeledDB_new", dir.name))
        for file in FileIt:
            fileType = os.path.splitext(os.path.realpath(file))[1]
            if fileType == ".obj" or fileType == ".off":
                totalMesh += 1
                mesh = Mesh(os.path.realpath(file))
                mesh.resample(expectedVerts, eps)
                mesh.saveMesh()
        FileIt.close()
    debugLog('Total mesh :' + str(totalMesh), debugLvl.DEBUG)


def dataVisualisation(list, feature, outputDir, n_bins=20, size_x=10, size_y=7):
    fig, axs = plt.subplots(1, 1, figsize=(size_x, size_y), tight_layout=True)

    plt.xlabel(feature)
    plt.ylabel("Number of mesh(es)")
    if(feature == dataName.SIDE_SIZE.value and outputDir=='output') : n_bins = [0.95+i*0.01 for i in range(11)]
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


# From a List of dictionnary retrieve a list of the element with key field of each dictionnary
def getFieldList(field,dictList):
    return [dict[field] for dict in dictList]


# From a List of List (listList) retrieve a list of the i-th element of each List
def getIndexList(i,listList, doAbs=False):
    if doAbs:
        return [abs(list[i]) for list in listList]
    else :
        return [list[i] for list in listList]

def plotDB(folder):
    dataIO = DataIO(folder)
    dataIO.plotHistograms([dataName.CATEGORY, dataName.FACE_NUMBERS, dataName.VERTEX_NUMBERS, dataName.SIDE_SIZE, dataName.DIST_BARYCENTER, dataName.PCA])