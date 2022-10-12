import csv
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from parse import getFieldList, getIndexList
from Mesh import Mesh
from dataName import dataName, dataDimension
from DebugLog import debugLvl, debugLog


class DBData:
    def __init__(self,outputDir):
        self.pctPath = "./"+outputDir+"/PRINCETON"
        self.lblPath = "./"+outputDir+"/LabeledDB"
        self.outputDir = outputDir
        self.dictList = []

    def exportData(self):
        meshesData1 = []
        for dir in os.scandir(self.lblPath):
            if os.path.isdir(dir):
                FileIt = os.scandir(os.path.join(self.lblPath, dir.name))
                for file in FileIt:
                    fileType = os.path.splitext(os.path.realpath(file))[1]
                    if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                        mesh = Mesh(os.path.realpath(file))
                        data = mesh.dataFilter()
                        meshesData1.append(data)
                FileIt.close()
        self.csvExport('dataLabeledDB.csv', meshesData1)

        meshesData2 = []
        for dir in os.scandir(self.pctPath):
            if os.path.isdir(dir):
                FileIt = os.scandir(os.path.join(self.pctPath, dir.name))
                for file in FileIt:
                    fileType = os.path.splitext(os.path.realpath(file))[1]
                    if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                        mesh = Mesh(os.path.realpath(file))
                        data = mesh.dataFilter()
                        meshesData2.append(data)
                FileIt.close()
        self.csvExport('dataPriceton.csv', meshesData2)
        self.dictList = meshesData1 + meshesData2

    def csvExport(self, fileName, data):
        filePath = os.path.join(os.path.realpath("./"+self.outputDir),fileName)
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        file = open(filePath, "w")
        csvDictWriter = csv.DictWriter(file, fieldnames=data[0].keys())
        csvDictWriter.writeheader()
        csvDictWriter.writerows(data)

    def plot(self, featuresList, n_bins=20, size_x=10, size_y=7):
        for feature in featuresList:
            dataVisualisation(getFieldList(feature, self.dictList), feature, self.outputDir, n_bins, size_x, size_y)

    def plot3D(self, featuresList):
        for feature in featuresList:
            if dataName.PCA.value == feature:
                mainComponentPCA = getIndexList(0, getFieldList(feature, self.dictList))
                XYZdataVisualisation(mainComponentPCA, feature, self.outputDir)
            else :
                XYZdataVisualisation(getFieldList(feature, self.dictList), feature, self.outputDir)

    def histograms(self, features):
        self.exportData()
        if dataName.CATEGORY in features :
            self.plot([dataName.CATEGORY.value], 26, 25, 10)
        oneD = [f.value for f in features if dataDimension[f] == 1 and f != dataName.CATEGORY]
        threeD = [f.value for f in features if dataDimension[f] == 3]
        if len(threeD) != 0: self.plot3D(threeD)
        if len(oneD) != 0: self.plot(oneD)


def normalise():
    totalMesh = 0
    for dir in os.scandir("./remesh/PRINCETON"):
        if os.path.isdir(dir):
            FileIt = os.scandir(os.path.join("./remesh/PRINCETON", dir.name))
            for file in FileIt:
                fileType = os.path.splitext(os.path.realpath(file))[1]
                if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                    totalMesh += 1
                    mesh = Mesh(os.path.realpath(file))
                    mesh.normalise()
                    mesh.saveMesh()
            FileIt.close()
    for dir in os.scandir("./remesh/LabeledDB"):
        if os.path.isdir(dir):
            FileIt =os.scandir(os.path.join("./remesh/LabeledDB", dir.name))
            for file in FileIt:
                fileType = os.path.splitext(os.path.realpath(file))[1]
                if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
                    totalMesh += 1
                    mesh = Mesh(os.path.realpath(file))
                    mesh.normalise()
                    mesh.saveMesh()
            FileIt.close()
    debugLog('Total mesh :' + str(totalMesh), debugLvl.DEBUG)


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
    dataIO = DBData(folder)
    dataIO.histograms([dataName.VERTEX_NUMBERS, dataName.SIDE_SIZE, dataName.DIST_BARYCENTER])