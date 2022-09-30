import csv
import os
import filter
import matplotlib.pyplot as plt


def exportMeshesData():
    pricetonPath = "./Models/PRINCETON/test"
    LabeledPath = "./Models/LabeledDB_new"
    meshesData1 = []

    for dir in os.scandir(LabeledPath):
        print(dir.name)
        FileIt =os.scandir(os.path.join(LabeledPath, dir.name))
        for file in FileIt:
            data = filter.dataFilter(os.path.realpath(file))
            if data is not None :
                meshesData1.append(data)
        FileIt.close()
    writeData('dataLabeledDB.csv',meshesData1)

    meshesData2 = []
    for dir in os.scandir(pricetonPath):
        print(dir.name)
        FileIt =os.scandir(os.path.join(pricetonPath, dir.name))
        for file in FileIt:
            data = filter.dataFilter(os.path.realpath(file))
            if data is not None:
                meshesData2.append(data)
        FileIt.close()
    writeData('dataPriceton.csv',meshesData2)

    return meshesData1 + meshesData2


def writeData(filename,data):
    try:
        file = open("./"+filename, 'w')
    except:
        print("Impossible to open :" + filename)
    csvDictWriter = csv.DictWriter(file, fieldnames=['Category', 'Face numbers', 'Vertex numbers', 'Bounding Box Diagonal Size','Types of faces'])
    csvDictWriter.writeheader()
    csvDictWriter.writerows(data)


def getValuesList(field,dictList):
    return [dict[field] for dict in dictList]


def dataVisualisation(list, feature, n_bins = 20,size_x=10, size_y=7):

    fig, axs = plt.subplots(1, 1,figsize=(size_x, size_y),tight_layout=True)

    plt.xlabel(feature)
    plt.ylabel("Number of mesh(es)")
    plt.title('Numbers of meshes depending on '+feature.lower())

    axs.hist(list, bins=n_bins)

    plt.savefig(feature.lower()+'.png')


def plotFeatures(dictList,featuresList, n_bins=20, size_x=10, size_y=7):
    for feature in featuresList:
        dataVisualisation(getValuesList(feature,dictList),feature, n_bins,size_x, size_y)
