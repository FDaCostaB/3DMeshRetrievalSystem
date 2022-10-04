import csv
import os
import matplotlib.pyplot as plt
import math
import pymeshlab
import numpy as np
from pathlib import Path

import MeshManip


def dataFilter(path):
    p1 = Path(path)
    category = os.path.relpath(p1.parent, p1.parent.parent)
    fileType = p1.suffix
    ms = pymeshlab.MeshSet()
    if(fileType == ".obj" or fileType == ".off"):
        ms.load_new_mesh(path)
        cur = ms.current_mesh()
        sizeFace = {}
        for face in cur.polygonal_face_list():
            if sizeFace.get(str(len(face))) is not None:
                sizeFace[str(len(face))] += 1
            else:
                sizeFace[str(len(face))] = 1
            if len(face)==4 : raise Exception("Quads found")
        diagSize = math.sqrt(cur.bounding_box().dim_x()+cur.bounding_box().dim_y()+cur.bounding_box().dim_z())
        res = {"Category" : category, "Face numbers" : cur.face_number(), "Vertex numbers" : cur.vertex_number(), "Bounding Box Diagonal Size" : diagSize, "Moment order" : momentOrder(cur), "Types of faces" : sizeFace}
        ms.clear()
        return res

def length(a,b):
    x = 0
    y = 1
    z = 2
    return ((b[x] - a[x])**2 + (b[y] - a[y])**2 + (b[z] - a[z])**2)**0.5
def momentOrder(mesh):
    faces = mesh.face_matrix()
    vertex = mesh.vertex_matrix()
    acc=[0,0,0]
    for tri in faces:
        x = 0
        y = 1
        z = 2
        a = vertex[tri[0]]
        b = vertex[tri[1]]
        c = vertex[tri[2]]
        ab = length(a,b)
        bc = length(b,c)
        ac = length(a,c)
        s = (ab+bc+ac) / 2
        area = (s*(s-ab)*(s-bc)*(s-ac))**0.5
        center = [(a[x]+b[x]+c[x])/3, (a[y]+b[y]+c[y])/3, (a[z]+b[z]+c[z])/3]
        acc[x] += area * np.sign(center[x])*(center[x])**2
        acc[y] += area * np.sign(center[y])*(center[y])**2
        acc[z] += area * np.sign(center[z])*(center[z])**2
    return acc

def dataMeshFilter(mesh):
    diagSize = math.sqrt(mesh.bounding_box().dim_x()+mesh.bounding_box().dim_y()+mesh.bounding_box().dim_z())
    res = {"Face numbers" : mesh.face_number(), "Vertex numbers" : mesh.vertex_number(), "Bounding Box Diagonal Size" : diagSize, "Moment order" : momentOrder(mesh),"PymeshLab Diag": mesh.bounding_box().diagonal(),"Size": [mesh.bounding_box().dim_x(),mesh.bounding_box().dim_y(),mesh.bounding_box().dim_z()]}
    return res

def exportMeshesData():
    pricetonPath = "./Models/PRINCETON/test"
    LabeledPath = "./Models/LabeledDB_new"
    meshesData1 = []

    for dir in os.scandir(LabeledPath):
        FileIt =os.scandir(os.path.join(LabeledPath, dir.name))
        for file in FileIt:
            data = dataFilter(os.path.realpath(file))
            if data is not None :
                meshesData1.append(data)
        FileIt.close()
    writeData('dataLabeledDB.csv',meshesData1)

    meshesData2 = []
    for dir in os.scandir(pricetonPath):
        FileIt =os.scandir(os.path.join(pricetonPath, dir.name))
        for file in FileIt:
            data = dataFilter(os.path.realpath(file))
            if data is not None:
                meshesData2.append(data)
        FileIt.close()
    writeData('dataPriceton.csv',meshesData2)

    return meshesData1 + meshesData2


def normaliseVertex(goal,eps):
    ms = pymeshlab.MeshSet()
    pricetonPath = "./Models/PRINCETON/test"
    LabeledPath = "./Models/LabeledDB_new"
    totalMesh = 0

    for dir in os.scandir(LabeledPath):
        FileIt =os.scandir(os.path.join(LabeledPath, dir.name))
        for file in FileIt:
            data = dataFilter(os.path.realpath(file))
            if data is not None:
                totalMesh += 1
                MeshManip.resample(os.path.realpath(file), './output', ms, goal, eps)
        FileIt.close()
    for dir in os.scandir(pricetonPath):
        FileIt =os.scandir(os.path.join(pricetonPath, dir.name))
        for file in FileIt:
            data = dataFilter(os.path.realpath(file))
            if data is not None:
                totalMesh += 1
                MeshManip.resample(os.path.realpath(file), './output', ms, goal, eps)
        FileIt.close()
    print(totalMesh)

def writeData(filename,data):
    try:
        file = open("./output/"+filename, 'w')
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

    plt.savefig("./output/"+feature.lower()+'.png')


def plotFeatures(dictList,featuresList, n_bins=20, size_x=10, size_y=7):
    for feature in featuresList:
        dataVisualisation(getValuesList(feature,dictList),feature, n_bins,size_x, size_y)
