import random
import os.path
import pymeshlab
import polyscope as ps
import numpy as np
from math import pi
import Math
from featureName import featureName, featureDimension, featureHistoBins, featureWeight, histoUpperBound
from parse import getIndexList
from pyemd import emd # https://pypi.org/project/pyemd/
from Settings import settings, settingsName


class FeaturesExtract:
    def __init__(self, meshPath):
        fileType = os.path.splitext(os.path.realpath(meshPath))[1]
        if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
            self.fileName = os.path.basename(meshPath)
            self.category = os.path.basename(os.path.dirname(meshPath))
            self.ms = pymeshlab.MeshSet()
            self.ms.load_new_mesh(meshPath)
            self.mesh = self.ms.current_mesh()
        else:
            raise Exception("Format not accepted")

# ---------------------------------------------------------------------------------------------- #
# ------------------------------------ Features computation ------------------------------------ #
# ---------------------------------------------------------------------------------------------- #

    def featureFilter(self,nbOfSample=None):
        res = { featureName.DIRNAME.value : self.category, featureName.FILENAME.value : self.fileName,
                featureName.CENTROID.value : Math.length(self.centroid()), featureName.SURFACE_AREA.value : self.surfaceArea(),
                featureName.VOLUME.value : self.volume(), featureName.COMPACTNESS.value : self.compactness(),
                featureName.SPHERICITY.value : self.sphericity(), featureName.RECTANGULARITY.value : self.rectangularity(),
                featureName.DIAMETER.value : self.diameter(), featureName.ECCENTRICITY.value : self.eccentricity()}

        if nbOfSample is None: nbOfSample = settings[settingsName.nbSample.value]
        A3 = self.A3(nbOfSample)
        for i in range(len(A3[0])):
            res["A3-"+str(i)] = A3[1][i]
        D1 = self.D1(nbOfSample)
        for i in range(len(D1[0])):
            res["D1-"+str(i)] = D1[1][i]
        D2 = self.D2(nbOfSample)
        for i in range(len(D2[0])):
            res["D2-"+str(i)] = D2[1][i]
        D3 = self.D3(nbOfSample)
        for i in range(len(D3[0])):
            res["D3-"+str(i)] = D3[1][i]
        D4 = self.D4(nbOfSample)
        for i in range(len(D4[0])):
            res["D4-" + str(i)] = D4[1][i]
        return res

    def A3(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        upperbound = int(sampleNum ** (1/3))+1
        for i in range(upperbound):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            for j in range(upperbound):
                i1 = random.randint(0, len(vertices) - 1)
                if i0==i1: continue
                v1 = vertices[i1]
                for k in range(upperbound):
                    i2 = random.randint(0, len(vertices) - 1)
                    if i0 == i1 or i0 == i2 or i1 == i2: continue
                    v2 = vertices[i2]
                    res.append(Math.angle(Math.vect(v0, v1), Math.vect(v0, v2)))
        y, binEdges = np.histogram(res, range=(0,histoUpperBound[featureName.A3.value]), bins=featureHistoBins[featureName.A3.value])
        x = 0.5 * (binEdges[1:] + binEdges[:-1])
        normalisedY = []
        for yVal in y:
            normalisedY.append(yVal / sum(y))
        return [x, normalisedY]

    def D1(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        for i in range(sampleNum):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            res.append(Math.length(v0))
        y, binEdges = np.histogram(res, range=(0,histoUpperBound[featureName.D1.value]), bins=featureHistoBins[featureName.D1.value])
        x = 0.5 * (binEdges[1:] + binEdges[:-1])
        normalisedY = []
        for yVal in y:
            normalisedY.append(yVal / sum(y))
        return [x, normalisedY]

    def D2(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        upperbound = int(sampleNum ** (1 / 2))+1
        for i in range(upperbound):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            for j in range(upperbound):
                i1 = random.randint(0, len(vertices) - 1)
                if i0 == i1: continue
                v1 = vertices[i1]
                res.append(Math.dist(v0, v1))
        y, binEdges = np.histogram(res, range=(0,histoUpperBound[featureName.D2.value]), bins=featureHistoBins[featureName.D2.value])
        x = 0.5 * (binEdges[1:] + binEdges[:-1])
        normalisedY = []
        for yVal in y:
            normalisedY.append(yVal / sum(y) )
        return [x, normalisedY]

    def D3(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        upperbound = int(sampleNum ** (1 / 3))+1
        for i in range(upperbound):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            for j in range(upperbound):
                i1 = random.randint(0, len(vertices) - 1)
                if i0 == i1: continue
                v1 = vertices[i1]
                for k in range(upperbound):
                    i2 = random.randint(0, len(vertices) - 1)
                    if i0 == i1 or i0 == i2 or i1 == i2: continue
                    v2 = vertices[i2]
                    res.append(Math.triangleAreaVector(Math.vect(v0, v1), Math.vect(v0, v2)) ** 0.5)
        y, binEdges = np.histogram(res, range=(0,histoUpperBound[featureName.D3.value]), bins=featureHistoBins[featureName.D3.value])
        x = 0.5 * (binEdges[1:] + binEdges[:-1])
        normalisedY = []
        for yVal in y:
            normalisedY.append(yVal / sum(y))
        return [x, normalisedY]

    def D4(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        upperbound = int(sampleNum ** (1 / 4))+1
        nbMiss=0
        for i in range(upperbound):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            for j in range(upperbound):
                i1 = random.randint(0, len(vertices) - 1)
                if i0 == i1: continue
                v1 = vertices[i1]
                for k in range(upperbound):
                    i2 = random.randint(0, len(vertices) - 1)
                    if i0 == i1 or i0 == i2 or i1 == i2: continue
                    v2 = vertices[i2]
                    for l in range(upperbound):
                        i3 = random.randint(0, len(vertices) - 1)
                        if i0 == i1 or i0 == i2 or i0 == i3 or i1 == i2 or i1 == i3 or i2 == i3: continue
                        v3 = vertices[i3]
                        vol = Math.tetrahedronVolume(Math.vect(v0, v1), Math.vect(v0, v2), Math.vect(v0, v3))
                        if not np.isnan(vol):
                            res.append(vol**(1/3))
                        else:
                            nbMiss += 1
        y, binEdges = np.histogram(res, range=(0,histoUpperBound[featureName.D4.value]), bins=featureHistoBins[featureName.D4.value])
        x = 0.5 * (binEdges[1:] + binEdges[:-1])
        normalisedY =[]
        for yVal in y:
            normalisedY.append(yVal/sum(y))
        return [x, normalisedY]


    def surfaceArea(self):
        vertices = self.ms.mesh(0).vertex_matrix()
        faces = self.ms.mesh(0).face_matrix()
        area = 0
        for triVerts in faces:
            area += Math.triangleArea(vertices[triVerts[0]], vertices[triVerts[1]], vertices[triVerts[2]])
        return area


    def volume(self):
        components, barycenter_cloud = self.getComponentsFaceList()
        faces = self.ms.mesh(0).face_matrix()
        vertices = self.ms.mesh(0).vertex_matrix()
        volume = 0
        for compInd in range(len(components)):
            compFaces = components[compInd]
            for faceInd in compFaces:
                triVerts = faces[faceInd]
                tetraVol=Math.tetrahedronVolume(Math.vect(barycenter_cloud[compInd], vertices[triVerts[0]]),
                                                 Math.vect(barycenter_cloud[compInd], vertices[triVerts[1]]),
                                                 Math.vect(barycenter_cloud[compInd], vertices[triVerts[2]]))
                volume += tetraVol
        return abs(volume)

    def call(self, funcName):
        if funcName==featureName.A3.value:
            return self.A3()
        elif funcName==featureName.D1.value:
            return self.D1()
        elif funcName==featureName.D2.value:
            return self.D2()
        elif funcName==featureName.D3.value:
            return self.D3()
        elif funcName==featureName.D4.value:
            return self.D4()
        elif funcName==featureName.SURFACE_AREA.value:
            return self.surfaceArea()
        elif funcName==featureName.VOLUME.value:
            return self.volume()
        elif funcName==featureName.CENTROID.value:
            return Math.length(self.centroid())
        elif funcName==featureName.RECTANGULARITY.value:
            return self.rectangularity()
        elif funcName==featureName.COMPACTNESS.value:
            return self.compactness()
        elif funcName==featureName.SPHERICITY.value:
            return self.sphericity()
        elif funcName==featureName.DIAMETER.value:
            return self.diameter()
        elif funcName== featureName.ECCENTRICITY.value:
            return self.eccentricity()

    # Returns list containing a list of face for each component
    def getComponentsFaceList(self):
        self.ms.compute_color_by_conntected_component_per_face()
        face_colors = self.mesh.face_color_matrix()
        components = []
        colors = []
        for face_i in range(len(face_colors)):
            fcolor = face_colors[face_i]
            find = False
            for i in range(len(colors)):
                color = colors[i]
                if fcolor[0] == color[0] and fcolor[1] == color[1] and fcolor[2] == color[2]:
                    components[i].append(face_i)
                    find = True
            if not find:
                colors.append([fcolor[0], fcolor[1], fcolor[2]])
                components.append([])
                components[len(components) - 1].append(face_i)
        barycenter_cloud = []
        for comp in components:
            barycenter_cloud.append(self.barycenter(comp))
        if settings[settingsName.debug.value]:
            ps.init()
            ps_cloud = ps.register_point_cloud("Component barycenter", np.array(barycenter_cloud), color=[1, 0, 0])
            ps_cloud.set_radius(0.01)
            ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix(),transparency=0.6)
            ps.show()
        return components, barycenter_cloud

    def centroid(self):
        vertexMat = self.mesh.vertex_matrix()
        centroid = [0, 0, 0]
        for vert in vertexMat:
            centroid[0] += vert[0]
            centroid[1] += vert[1]
            centroid[2] += vert[2]
        return [coord/len(vertexMat) for coord in centroid]

    def volumeOBB(self):
        min = self.mesh.bounding_box().min()
        max = self.mesh.bounding_box().max()
        return (max[0] - min[0]) * (max[1] - min[1]) * (max[2] - min[2])

    def rectangularity(self):
        return self.volume()/self.volumeOBB()

    def barycenter(self, faceList):
        sumX = 0
        sumY = 0
        sumZ = 0
        total = 0
        vertexMat = self.mesh.vertex_matrix()
        faceMat = self.mesh.face_matrix()
        for faceInd in faceList:
            for vertInd in faceMat[faceInd]:
                sumX += vertexMat[vertInd][0]
                sumY += vertexMat[vertInd][1]
                sumZ += vertexMat[vertInd][2]
                total += 1
        return [sumX / total, sumY / total, sumZ / total]

    def compactness(self):
        area = self.surfaceArea()
        volume = self.volume()
        c = (area ** 3 / (36 * pi * volume ** 2))
        return c

    def sphericity(self):
        return 1/self.compactness()

    def diameter(self):
        self.ms.generate_convex_hull()
        vertexMat = self.ms.current_mesh().vertex_matrix()
        diameter = 0
        for u in vertexMat:
            for v in vertexMat:
                dist = Math.dist(u,v)
                if dist > diameter:
                    diameter = dist
        self.ms.set_current_mesh(0)
        return diameter

    def boundingBox(self):
        min = self.mesh.bounding_box().min()
        max = self.mesh.bounding_box().max()
        vertex = [[min[0],min[1],min[2]], [min[0],max[1],min[2]], [min[0],max[1],max[2]], [min[0],min[1],max[2]],
                 [max[0],min[1],min[2]], [max[0],min[1],max[2]], [max[0],max[1],min[2]], [max[0],max[1],max[2]]]
        faces = [[0, 1, 2], [0,2,3], [0,3,4], [3, 4, 5], [1, 2, 6], [2, 6, 7], [2, 3, 5], [2, 5, 7], [0, 1, 4], [1, 4, 6], [4, 5, 6], [5, 6, 7]]
        return vertex, faces

    def eccentricity(self):
        vertexMat = self.mesh.vertex_matrix()
        V = np.zeros((3, len(vertexMat)))
        V[0] = getIndexList(0, vertexMat)
        V[1] = getIndexList(1, vertexMat)
        V[2] = getIndexList(2, vertexMat)

        V_cov = np.cov(V)
        eigenvalues, eigenvectors = np.linalg.eig(V_cov)
        return max(eigenvalues)/min(eigenvalues)

# ---------------------------------------------------------------------------------------------- #
# ---------------------------------------- I/O features ---------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

    def showBoundingBox(self):
        vertex, faces = self.boundingBox()
        ps.init()
        ps.register_point_cloud("Before cloud points", self.ms.mesh(0).vertex_matrix())
        ps.register_surface_mesh("Before Mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix())
        ps.register_surface_mesh("Bounding box", np.array(vertex), np.array(faces))
        ps.show()


def euclidianDist(f1, f2):
    sumDist = 0
    weight = 0
    distanceContribution = {"A3":0,"D1":0,"D2":0,"D3":0,"D4":0}
    for key in f1.keys():
        if key[:2]=="A3" or key[:2]=="D1" or key[:2]=="D2" or key[:2]=="D3" or key[:2]=="D4":
            featureDist = (featureWeight[key[:2]] / (sum(list(featureWeight.values())) * featureHistoBins[key[:2]])) * abs(f1[key] - f2[key]) ** 2
            weight += featureWeight[key[:2]] / (sum(list(featureWeight.values())) * featureHistoBins[key[:2]])
            sumDist += featureDist
            distanceContribution[key[:2]] += featureDist
        elif key not in ['File name', 'Folder name'] :
            featureDist = (featureWeight[key] / sum(list(featureWeight.values()))) * abs(f1[key] - f2[key]) ** 2
            weight += featureWeight[key] / sum(list(featureWeight.values()))
            sumDist += featureDist
            distanceContribution[key] = featureDist
    if weight > 1+1e-9 or weight < 1-1e-9:
        raise Exception("Sum of weight not equal to 1 - Sum : "+ str(weight))
    distanceContribution = {key: val for key,val in sorted(distanceContribution.items(), key = lambda ele: ele[1], reverse = True)}
    return sumDist**0.5, os.path.join(f1[featureName.DIRNAME.value],f1[featureName.FILENAME.value]), os.path.join(f2[featureName.DIRNAME.value],f2[featureName.FILENAME.value]), distanceContribution


def emDist(f1, f2):
    sumScalar = 0
    sumHisto = 0
    distanceContribution = {}
    for key in f1.keys():
        if key[:2] not in ['A3','D1','D2','D3','D4'] and key not in ['File name', 'Folder name']:
            featureDist = (featureWeight[key] / sum(list(featureWeight.values()))) * abs(f1[key] - f2[key]) ** 2
            sumScalar += featureDist
            distanceContribution[key] = featureDist
    for histoName in ['A3', 'D1', 'D2', 'D3', 'D4']:
        histf1 = np.array([list(f1.values())[i] for i in range(len(f1)) if list(f1.keys())[i][:2] == histoName])
        histf2 = np.array([list(f2.values())[i] for i in range(len(f2)) if list(f2.keys())[i][:2] == histoName])
        if len(histf1) != len(histf2):
            raise ("Dimmensionality is not the same")
        dist = Math.matrixDist(len(histf1),histoName)
        featureDist = (featureWeight[key[:2]] / sum(list(featureWeight.values()))) * abs(emd(histf1, histf2, dist))
        sumHisto += featureDist
        distanceContribution[histoName] = featureDist
    distanceContribution = {key: val for key,val in sorted(distanceContribution.items(), key = lambda ele: ele[1], reverse = True)}
    return sumScalar ** 0.5 + sumHisto, os.path.join(f1[featureName.DIRNAME.value],f1[featureName.FILENAME.value]), os.path.join(f2[featureName.DIRNAME.value],f2[featureName.FILENAME.value]), distanceContribution
