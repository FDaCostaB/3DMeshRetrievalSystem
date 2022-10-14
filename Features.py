import random
import os.path
import pymeshlab
import polyscope as ps
import numpy as np
import Math


class FeaturesExtract:
    def __init__(self, meshPath):
        fileType = os.path.splitext(os.path.realpath(meshPath))[1]
        if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
            self.meshPath = meshPath
            self.ms = pymeshlab.MeshSet()
            self.ms.load_new_mesh(meshPath)
            self.mesh = self.ms.current_mesh()
            self.category = os.path.dirname(meshPath)
        else:
            raise Exception("Format not accepted")


# ---------------------------------------------------------------------------------------------- #
# ------------------------------------ Features computation ------------------------------------ #
# ---------------------------------------------------------------------------------------------- #
    def A3(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        upperbound = int(sampleNum ** (1/3))+1
        for i in range(upperbound):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            for j in range(upperbound):
                i1 = random.randint(0, len(vertices) - 1)
                if i0==i1: break
                v1 = vertices[i1]
                for k in range(upperbound):
                    i2 = random.randint(0, len(vertices) - 1)
                    if i0 == i1 or i0 == i2 or i1 == i2: break
                    v2 = vertices[i2]
                    res.append(Math.angle(Math.vect(v0, v1), Math.vect(v0, v2)))
        return res


    def D1(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        for i in range(sampleNum):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            res.append(Math.length(v0))
        return res


    def D2(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        upperbound = int(sampleNum ** (1 / 2))+1
        for i in range(upperbound):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            for j in range(upperbound):
                i1 = random.randint(0, len(vertices) - 1)
                if i0 == i1 : break
                v1 = vertices[i1]
                res.append(Math.dist(v0, v1))
        return res


    def D3(self, sampleNum=100000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        upperbound = int(sampleNum ** (1 / 3))+1
        for i in range(upperbound):
            i0 = random.randint(0, len(vertices) - 1)
            v0 = vertices[i0]
            for j in range(upperbound):
                i1 = random.randint(0, len(vertices) - 1)
                if i0 == i1  : break
                v1 = vertices[i1]
                for k in range(upperbound):
                    i2 = random.randint(0, len(vertices) - 1)
                    if i0 == i1 or i0 == i2 or i1 == i2: break
                    v2 = vertices[i2]
                    res.append(Math.triangleAreaVector(Math.vect(v0, v1), Math.vect(v0, v2)) ** 0.5)
        return res


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
                if i0 == i1: break
                v1 = vertices[i1]
                for k in range(upperbound):
                    i2 = random.randint(0, len(vertices) - 1)
                    if i0 == i1 or i0 == i2 or i1 == i2: break
                    v2 = vertices[i2]
                    for l in range(upperbound):
                        i3 = random.randint(0, len(vertices) - 1)
                        if i0 == i1 or i0 == i2 or i0 == i3 or i1 == i2 or i1 == i3 or i2 == i3: break
                        v3 = vertices[i3]
                        vol = Math.tetrahedronVolume(Math.vect(v0, v1), Math.vect(v0, v2), Math.vect(v0, v3))
                        if not np.isnan(vol**(1/3)):
                            res.append(vol**(1/3))
                        else:
                            nbMiss += 1
        return res


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
                volume += abs(tetraVol)
        return volume

    def call(self, funcName):
        if funcName=="A3":
            return self.A3()
        elif funcName=="D1":
            return self.D1()
        elif funcName=="D2":
            return self.D2()
        elif funcName=="D3":
            return self.D3()
        elif funcName=="D4":
            return self.D4()
        elif funcName=="surfaceArea":
            return self.surfaceArea()
        elif funcName=="volume":
            return self.volume()

    # Returns list containing a list of face for each component
    def getComponentsFaceList(self, debug=False):
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
        if debug:
            ps.init()
            ps_cloud = ps.register_point_cloud("Component barycenter", np.array(barycenter_cloud), color=[1, 0, 0])
            ps_cloud.set_radius(0.01)
            ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix(),transparency=0.6)
            ps.show()
        return components, barycenter_cloud


    def barycenter(self, faceList):
        sumX = 0;
        sumY = 0;
        sumZ = 0;
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
        c = (area ** 3 / (36 * Math.pi * volume ** 2))
        return c

# ---------------------------------------------------------------------------------------------- #
# ---------------------------------------- I/O features ---------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

    def silhouetteExport(self):
        os.makedirs('./screenshot', exist_ok=True)
        fileName = os.path.splitext(os.path.basename(self.meshPath))[0]
        ps.init()
        ps.set_ground_plane_mode("none")
        ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix(), material='flat',
                                 color=[0, 0, 0])
        ps.set_view_projection_mode("orthographic")
        ps.set_screenshot_extension(".jpg");
        ps.set_up_dir("x_up")
        ps.screenshot('./screenshot/' + fileName + '_x.jpg', False)
        ps.set_up_dir("y_up")
        ps.screenshot('./screenshot/' + fileName + '_y.jpg', False)
        ps.set_up_dir("z_up")
        ps.screenshot('./screenshot/' + fileName + '_z.jpg', False)
