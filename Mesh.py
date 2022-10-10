import os.path
import pymeshlab
import Math
import polyscope as ps
import numpy as np
from pathlib import Path
from dataName import dataName
from Debug import debugLvl, debugLog
import random

class Mesh:
    def __init__(self, meshPath):
        self.meshPath = meshPath
        self.ms = pymeshlab.MeshSet()
        self.ms.load_new_mesh(meshPath)
        self.mesh = self.ms.current_mesh()
        self.expectedVerts = 10000
        self.eps = 1000

    def dataFilter(self):
        p1 = Path(self.meshPath)
        category = os.path.relpath(p1.parent, p1.parent.parent)
        fileType = os.path.splitext(os.path.realpath(self.meshPath))[1]
        if fileType == ".obj" or fileType == ".off" :
            for face in self.mesh.polygonal_face_list():
                if len(face)==4 : raise Exception("Quads found")
            out_dict = self.ms.get_geometric_measures()
            size = [ self.mesh.bounding_box().dim_x(), self.mesh.bounding_box().dim_y(), self.mesh.bounding_box().dim_z()]
            res = {dataName.CATEGORY.value : category, dataName.FACE_NUMBERS.value : self.mesh.face_number(), dataName.VERTEX_NUMBERS.value : self.mesh.vertex_number(),
                   dataName.SIDE_SIZE.value : max(size), dataName.MOMENT.value : self.momentOrder(), dataName.SIZE.value : size, dataName.BARYCENTER.value : list(out_dict['shell_barycenter']),
                   dataName.DIST_BARYCENTER.value : Math.length(list(out_dict['shell_barycenter'])),dataName.PCA.value :list(out_dict['pca']), dataName.DIAGONAL.value : self.mesh.bounding_box().diagonal()}
            return res

    def refine(self, expectedVerts=None, eps=None):
        LIMIT = 5
        if expectedVerts is None: expectedVerts = self.expectedVerts
        else: self.expectedVerts = expectedVerts
        if eps is None: eps = self.eps
        else: self.eps = eps


        oldStats = self.dataFilter()
        newStats = self.dataFilter()

        # Subdivide vertix up to five time to get in range [expectedVerts - eps, expectedVerts + eps]
        i = 0
        while (newStats[dataName.VERTEX_NUMBERS.value] < expectedVerts - eps and i < LIMIT):
            if newStats[dataName.VERTEX_NUMBERS.value] < self.expectedVerts - self.eps:
                try:
                    self.ms.apply_filter('meshing_surface_subdivision_loop', iterations=1)
                except:
                    self.ms.apply_filter('meshing_repair_non_manifold_edges', method='Remove Faces')
                    self.ms.apply_filter('meshing_repair_non_manifold_vertices')
                    debugLog(os.path.realpath(self.meshPath) + " - ERROR : Failed to apply filter:  'meshing_surface_subdivision_loop' => Applying Non-Manifold Repair",debugLvl.ERROR)
            newStats = self.dataFilter()
            i += 1

        # Decimation (merging vertex) to reduce in range [expectedVerts - eps, expectedVerts + eps]
        if newStats[dataName.VERTEX_NUMBERS.value] > self.expectedVerts + self.eps:
            self.ms.apply_filter('meshing_decimation_quadric_edge_collapse',targetperc=self.expectedVerts / newStats[dataName.VERTEX_NUMBERS.value])
        newStats = self.dataFilter()

        # Laplacian smooth to get a more uniformly distributed point cloud over the mesh
        try:
            self.ms.apply_filter('apply_coord_laplacian_smoothing', stepsmoothnum=3)
        except:
            debugLog(os.path.realpath(self.meshPath) + " - ERROR : Failed to apply filter:  'apply_coord_laplacian_smoothing.",debugLvl.ERROR)
        if newStats[dataName.VERTEX_NUMBERS.value] < self.expectedVerts - self.eps or newStats[
            dataName.VERTEX_NUMBERS.value] > self.expectedVerts + self.eps:
            debugLog(os.path.realpath(self.meshPath) + ' : Before - ' + str(oldStats[dataName.VERTEX_NUMBERS.value]) +
                     ' | After - ' + str(newStats[dataName.VERTEX_NUMBERS.value]), debugLvl.WARNING)

    def momentOrder(self):
        faces = self.mesh.face_matrix()
        vertex = self.mesh.vertex_matrix()
        acc = [0, 0, 0]
        x = 0
        y = 1
        z = 2
        for tri in faces:
            a = vertex[tri[0]]
            b = vertex[tri[1]]
            c = vertex[tri[2]]
            center = [(a[x] + b[x] + c[x]) / 3, (a[y] + b[y] + c[y]) / 3, (a[z] + b[z] + c[z]) / 3]
            acc[x] += np.sign(center[x]) * (center[x]) ** 2
            acc[y] += np.sign(center[y]) * (center[y]) ** 2
            acc[z] += np.sign(center[z]) * (center[z]) ** 2
        return acc

    def swapAxis(self):
        stats = self.dataFilter()
        pca = stats[dataName.PCA.value]
        for i in range(3):
            maxInd = 0
            for j in range(0,3):
                if abs(float(pca[j][i])) >= abs(float(pca[maxInd][i])) :
                    maxInd = j
            if maxInd != i :
                if (i==0 and maxInd==1) or (i==1 and maxInd==0):
                    self.ms.compute_matrix_from_rotation(rotaxis='Z axis', rotcenter='barycenter', angle=90)
                elif (i==0 and maxInd==2) or (i==2 and maxInd==1):
                    self.ms.compute_matrix_from_rotation(rotaxis='Y axis', rotcenter='barycenter', angle=90)
                elif (i==1 and maxInd==2) or (i==2 and maxInd==1):
                    self.ms.compute_matrix_from_rotation(rotaxis='X axis', rotcenter='barycenter', angle=90)
                stats = self.dataFilter()
                pca = stats[dataName.PCA.value]

    def flipMomentTest(self, doDebug=False):
        moment = self.momentOrder()
        if (moment[0] < 0 and doDebug):
            self.ms.compute_matrix_from_rotation(rotaxis='X axis',rotcenter='barycenter',angle=180)
            debugLog(os.path.realpath(self.meshPath) + ' : Flip x axis',debugLvl.DEBUG)
        if (moment[1] < 0 and doDebug):
            self.ms.compute_matrix_from_rotation(rotaxis='Y axis', rotcenter='barycenter', angle=180)
            debugLog(os.path.realpath(self.meshPath) + ' : Flip y axis',debugLvl.DEBUG)
        if (moment[2] < 0 and doDebug):
            self.ms.compute_matrix_from_rotation(rotaxis='Z axis', rotcenter='barycenter', angle=180)
            debugLog(os.path.realpath(self.meshPath) + ' : Flip z axis',debugLvl.DEBUG)

    def normalise(self, showDebug=False):
        stats = self.dataFilter()
        if (showDebug):
            self.printProperties()

        self.ms.compute_matrix_from_translation(traslmethod='XYZ translation', axisx=-1 * stats[dataName.BARYCENTER.value][0],
                                           axisy=-1 * stats[dataName.BARYCENTER.value][1],
                                           axisz=-1 * stats[dataName.BARYCENTER.value][2])
        self.ms.compute_matrix_by_principal_axis()
        self.swapAxis()
        self.flipMomentTest(showDebug)
        stats = self.dataFilter()
        self.ms.compute_matrix_from_scaling_or_normalization(axisx=1/stats[dataName.SIDE_SIZE.value],scalecenter='barycenter', uniformflag=True)

        if (showDebug):
            self.printProperties()
            self.compare()

    def resample(self, expectedVerts=10000, eps=1000, showComparison=False):
        # if showComparison:
        #    self.printProperties()

        self.ms.apply_filter('meshing_remove_duplicate_faces')
        self.ms.apply_filter('meshing_remove_duplicate_vertices')
        self.ms.apply_filter('meshing_remove_unreferenced_vertices')
        self.expectedVerts = expectedVerts
        self.eps = eps
        self.refine()
        self.normalise()

        if showComparison:
            self.printProperties()
            self.compare()

    def compare(self):
        if len(self.ms) == 1 :
            self.ms.load_new_mesh(self.meshPath)
            self.ms.set_current_mesh(0)
        ps.init()
        ps.register_point_cloud("Before cloud points", self.ms.mesh(1).vertex_matrix())
        ps.register_surface_mesh("Before Mesh", self.ms.mesh(1).vertex_matrix(), self.ms.mesh(1).face_matrix())
        ps.register_point_cloud("After cloud points", self.ms.mesh(0).vertex_matrix())
        ps.register_surface_mesh("After Mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix())
        ps.show()

    def A3(self, sampleNum=10000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        for i in range(sampleNum):
            i0 = random.randint(0,len(vertices)-1)
            i1 = random.randint(0,len(vertices)-1)
            i2 = random.randint(0,len(vertices)-1)
            res.append(Math.angle(Math.vect(i1, i0), Math.vect(i1, i2)))
        return res

    def D1(self, sampleNum=10000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        for i in range(sampleNum):
            i0 = random.randint(0,len(vertices)-1)
            res.append(Math.length(i0))
        return res

    def D2(self, sampleNum=10000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        for i in range(sampleNum):
            i0 = random.randint(0, len(vertices) - 1)
            i1 = random.randint(0, len(vertices) - 1)
            res.append(Math.dist(i0, i1))
        return res

    def D3(self, sampleNum=10000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        for i in range(sampleNum):
            i0 = random.randint(0, len(vertices) - 1)
            i1 = random.randint(0, len(vertices) - 1)
            i2 = random.randint(0, len(vertices) - 1)
            res.append(Math.triangleArea(i0, i1, i2)**0.5)
        return res

    def D4(self, sampleNum=10000):
        vertices = self.ms.mesh(0).vertex_matrix()
        res = []
        for i in range(sampleNum):
            i0 = random.randint(0, len(vertices) - 1)
            i1 = random.randint(0, len(vertices) - 1)
            i2 = random.randint(0, len(vertices) - 1)
            i3 = random.randint(0, len(vertices) - 1)
            res.append(Math.tetrahedronVolume(Math.vect(i0, i1), Math.vect(i0, i2), Math.vect(i0, i3))**(1/3))
        return res

    def surfaceArea(self):
        vertices = self.ms.mesh(0).vertex_matrix()
        faces = self.ms.mesh(0).face_matrix()
        area = 0
        for faceInd in faces:
            for vertInd in faces[faceInd]:
                vert = vertices[vertInd]
                area += Math.triangleArea(vert[0], vert[1], vert[2])
        return area

    def volume(self):
        components, barycenter_cloud = self.getComponentsFaceList()
        vertices = self.ms.mesh(0).vertex_matrix()
        volume = 0
        for compInd in range(len(components)):
            faces = components[compInd]
            for faceInd in faces:
                for vertInd in faces[faceInd]:
                    volume += Math.tetrahedronVolume(Math.vect(barycenter_cloud[compInd],vertices[vertInd][0]),
                                           Math.vect(barycenter_cloud[compInd],vertices[vertInd][1]), Math.vect(barycenter_cloud[compInd],vertices[vertInd][2]))
        return volume

    #Returns list containing a list of face for each components
    def getComponentsFaceList(self, debug=False):
        self.ms.compute_color_by_conntected_component_per_face()
        face_colors = self.mesh.face_color_matrix()
        components = []
        colors=[]
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
                components[len(components)-1].append(face_i)
        barycenter_cloud = []
        for comp in components:
            barycenter_cloud.append(self.barycenter(comp))
        if debug :
            ps.init()
            ps_cloud = ps.register_point_cloud("Component barycenter", np.array(barycenter_cloud), color=[1, 0, 0])
            ps_cloud.set_radius(0.01)
            ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix(), transparency=0.6)
            ps.show()
        return components, barycenter_cloud

    def barycenter(self, faceList):
        sumX=0; sumY=0; sumZ=0; total=0;
        vertexMat = self.ms.mesh(0).vertex_matrix()
        faceMat = self.ms.mesh(0).face_matrix()
        for faceInd in faceList:
            for vertInd in faceMat[faceInd]:
                sumX += vertexMat[vertInd][0]
                sumY += vertexMat[vertInd][1]
                sumZ += vertexMat[vertInd][2]
                total += 1
        return [sumX/total, sumY/total, sumZ/total]
    # ----- I/O features -----

    def printProperties(self):
        stats = self.dataFilter()
        debugLog(
            os.path.realpath(self.meshPath) + ' : Size :' + str(stats[dataName.SIDE_SIZE.value]) + ', Shell Barycenter : ' + str(stats[dataName.BARYCENTER.value]) + ', Moment order' +
            str(np.sign(stats[dataName.MOMENT.value])) +'\nPCA :\n'+ str(stats[dataName.PCA.value]),debugLvl.DEBUG)

    def saveMesh(self):
        # Same path with output instead of Model
        newPath = os.path.join('./output',os.path.relpath(self.meshPath,'./Models'))

        #Create parent dir if it doesn't exist
        os.makedirs(os.path.dirname(newPath), exist_ok=True)

        #Save the file in off format
        self.ms.save_current_mesh(os.path.splitext(newPath)[0]+".off")

    def render(self):
        ps.init()
        ps_cloud = ps.register_point_cloud("my points", self.ms.mesh(0).vertex_matrix())
        ps_cloud.set_radius(0.002)
        ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix())
        ps.show()

    def silhouetteExport(self):
        os.makedirs('./screenshot', exist_ok=True)
        fileName = os.path.splitext(os.path.basename(self.meshPath))[0]
        ps.init()
        ps.set_ground_plane_mode("none")
        ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix(), material='flat',color=[0,0,0])
        ps.set_view_projection_mode("orthographic")
        ps.set_screenshot_extension(".jpg");
        ps.set_up_dir("x_up")
        ps.screenshot('./screenshot/'+fileName+'_x.jpg', False)
        ps.set_up_dir("y_up")
        ps.screenshot('./screenshot/'+fileName+'_y.jpg', False)
        ps.set_up_dir("z_up")
        ps.screenshot('./screenshot/'+fileName+'_z.jpg', False)
