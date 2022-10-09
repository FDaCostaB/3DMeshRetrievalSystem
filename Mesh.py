import os.path
import pymeshlab
import Math
import polyscope as ps
import numpy as np
from pathlib import Path
from dataName import dataName
from Debug import debugLvl,debugLog

class Mesh:
    def __init__(self,meshPath):
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
                   dataName.DIST_BARYCENTER.value : Math.dist(list(out_dict['shell_barycenter'])),dataName.PCA.value :list(out_dict['pca']), dataName.DIAGONAL.value : self.mesh.bounding_box().diagonal()}
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
        ps.register_point_cloud("my points", self.ms.mesh(0).vertex_matrix())
        ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix())
        ps.show()