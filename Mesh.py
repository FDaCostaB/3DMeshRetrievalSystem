import os.path
from pathlib import Path
import pymeshlab
import polyscope as ps
import numpy as np
from dataName import dataName
from parse import getIndexList
import polyscopeUI as psUI
import Math
from Settings import settings,settingsName,readSettings

class Mesh:
    def __init__(self, meshPath):
        fileType = os.path.splitext(os.path.realpath(meshPath))[1]
        if fileType == ".obj" or fileType == ".off" or fileType == ".ply":
            self.meshPath = meshPath
            self.ms = pymeshlab.MeshSet()
            self.ms.load_new_mesh(meshPath)
            self.mesh = self.ms.current_mesh()
        else:
            raise Exception("Format not accepted : "+ fileType)

    # ---------------------------------------------------------------------------------------------- #
    # --------------------------------- Normalisation computations --------------------------------- #
    # ---------------------------------------------------------------------------------------------- #
    def dataFilter(self):
        p1 = Path(self.meshPath)
        category = os.path.relpath(p1.parent, p1.parent.parent)
        for face in self.mesh.polygonal_face_list():
            if len(face)==4 : print("--------------------------------------Quads found--------------------------------------")
        out_dict = self.ms.get_geometric_measures()
        eigenvalues, eigenvectors = self.getPCA()
        size = [ self.mesh.bounding_box().dim_x(), self.mesh.bounding_box().dim_y(), self.mesh.bounding_box().dim_z()]
        res = {dataName.CATEGORY.value : category, dataName.FACE_NUMBERS.value : self.mesh.face_number(), dataName.VERTEX_NUMBERS.value : self.mesh.vertex_number(),
               dataName.SIDE_SIZE.value : max(size), dataName.MOMENT.value : self.momentOrder(), dataName.SIZE.value : size, dataName.BARYCENTER.value : out_dict['barycenter'],
               dataName.DIST_BARYCENTER.value : Math.length(out_dict['barycenter']), dataName.PCA.value : eigenvectors, dataName.EIGENVALUES.value : eigenvalues,
               dataName.DIAGONAL.value : self.mesh.bounding_box().diagonal(), dataName.COMPONENTS_NUMBER.value : self.getNbComponents() }
        return res

    def normaliseVertices(self):
        LIMIT = 5
        i = 0
        readSettings()
        expectedVerts = settings[settingsName.expectedVerts.value]
        eps = settings[settingsName.epsVerts.value]

        oldStats = self.dataFilter()
        newStats = self.dataFilter()
        while (newStats[dataName.VERTEX_NUMBERS.value] < expectedVerts - eps and i < LIMIT):
            if newStats[dataName.VERTEX_NUMBERS.value] < expectedVerts - eps:
                try:
                    self.ms.apply_filter('meshing_surface_subdivision_loop', threshold=pymeshlab.Percentage(0), iterations=1)
                except:
                    self.ms.apply_filter('meshing_repair_non_manifold_edges', method='Remove Faces')
                    self.ms.apply_filter('meshing_repair_non_manifold_vertices')
            elif newStats[dataName.VERTEX_NUMBERS.value] > expectedVerts + eps:
                self.ms.apply_filter('meshing_decimation_quadric_edge_collapse', targetperc= expectedVerts / newStats[dataName.VERTEX_NUMBERS.value])
            newStats = self.dataFilter()
            i += 1

        # Extra turn of decimation (merging vertex) to reduce in range if laste iteration subdivide to above the range
        # Decimation (merging vertex) to reduce in range [expectedVerts - eps, expectedVerts + eps]
        if newStats[dataName.VERTEX_NUMBERS.value] > expectedVerts:
            self.ms.apply_filter('meshing_decimation_quadric_edge_collapse',targetperc=expectedVerts / newStats[dataName.VERTEX_NUMBERS.value])

        newStats = self.dataFilter()
        # Laplacian smooth to get a more uniformly distributed point cloud over the mesh
        try:
            self.ms.apply_filter('apply_coord_laplacian_smoothing', stepsmoothnum=5)
        except:
            print(os.path.realpath(self.meshPath) + " - ERROR : Failed to apply filter:  'apply_coord_laplacian_smoothing.")

    def clean(self):
        self.ms.apply_filter('meshing_remove_duplicate_faces')
        self.ms.apply_filter('meshing_remove_duplicate_vertices')
        self.ms.apply_filter('meshing_remove_unreferenced_vertices')

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
            acc[x] += np.sign(center[x]) * center[x] ** 2
            acc[y] += np.sign(center[y]) * center[y] ** 2
            acc[z] += np.sign(center[z]) * center[z] ** 2
        return acc

    def principalAxisAlignement(self, doDebug=False):
        stats = self.dataFilter()
        pca = stats[dataName.PCA.value]
        for vect in pca:
            vect[0] = vect[0]/Math.length(vect)
            vect[1] = vect[1]/Math.length(vect)
            vect[2] = vect[2]/Math.length(vect)
        facesMat = self.mesh.face_matrix()
        vertexMat = self.mesh.vertex_matrix()
        edgesMat = self.mesh.edge_matrix()
        for i in range(len(vertexMat)) :
            vertexMat[i] = [Math.dotProduct(pca[0],vertexMat[i]), Math.dotProduct(pca[1],vertexMat[i]), Math.dotProduct(pca[2],vertexMat[i])]

        transformedMesh = pymeshlab.Mesh(vertex_matrix=vertexMat, face_matrix=facesMat,edge_matrix=edgesMat)
        self.ms.clear()
        self.ms.add_mesh(transformedMesh)
        self.mesh = self.ms.current_mesh()

    def flipMomentTest(self, doDebug=False):
        moment = np.sign(self.momentOrder())
        facesMat = self.mesh.face_matrix()
        vertexMat = self.mesh.vertex_matrix()
        edgesMat = self.mesh.edge_matrix()
        for i in range(len(vertexMat)) :
            vertexMat[i] = [vertexMat[i][0]*moment[0], vertexMat[i][1]*moment[1], vertexMat[i][2]*moment[2]]
        transformedMesh = pymeshlab.Mesh(vertex_matrix=vertexMat, face_matrix=facesMat,edge_matrix=edgesMat )
        self.ms.clear()
        self.ms.add_mesh(transformedMesh)
        self.mesh = self.ms.current_mesh()

    def normalise(self, showComparison=False):
        stats = self.dataFilter()
        self.ms.compute_matrix_from_translation(traslmethod='XYZ translation', axisx=-1 * stats[dataName.BARYCENTER.value][0],
                                           axisy=-1 * stats[dataName.BARYCENTER.value][1],
                                           axisz=-1 * stats[dataName.BARYCENTER.value][2])
        self.principalAxisAlignement()
        self.flipMomentTest()
        stats = self.dataFilter()
        self.ms.compute_matrix_from_scaling_or_normalization(axisx=1 / stats[dataName.SIDE_SIZE.value],
                                                             customcenter=stats[dataName.BARYCENTER.value],
                                                             uniformflag=True)

        if showComparison:
            self.compare()

    def resample(self, showComparison=False):

        self.clean()
        self.normaliseVertices()
        self.normalise()

        if showComparison:
            self.compare()

    def getNbComponents(self):
        self.ms.compute_color_by_conntected_component_per_face()
        face_colors = self.mesh.face_color_matrix()
        colors = []

        # traverse for all elements
        for fcolor in face_colors:
            found = False
            for color in colors:
                if fcolor[0] == color[0] and fcolor[1] == color[1] and fcolor[2] == color[2]:
                    found=True
            if len(colors) == 0 or not found:
                colors.append(fcolor)
        return len(colors)

    def getPCA(self):
        vertexMat = self.mesh.vertex_matrix()
        V = np.zeros((3, len(vertexMat)))
        V[0] = getIndexList(0,vertexMat)
        V[1] = getIndexList(1,vertexMat)
        V[2] = getIndexList(2,vertexMat)

        V_cov = np.cov(V)
        eigenvalues, eigenvectors = np.linalg.eig(V_cov)
        res=[getIndexList(0,eigenvectors),getIndexList(1,eigenvectors), getIndexList(2,eigenvectors)]

        for i in range (3):
            for j in range(i+1,3):
                if(eigenvalues[j]>eigenvalues[i]):
                   temp=res[i].copy()
                   res[i] = res[j]
                   res[j] = temp
                   temp=eigenvalues[i]
                   eigenvalues[i] = eigenvalues[j]
                   eigenvalues[j] = temp

        return eigenvalues, [res[0],res[1],Math.crossProduct(res[0],res[1])]
# ---------------------------------------------------------------------------------------------- #
# ---------------------------------------- I/O features ---------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

    def compare(self):
        psUI.setPolyscopeSetting(1280, 720)
        if len(self.ms) == 1 :
            self.ms.load_new_mesh(self.meshPath)
            self.ms.set_current_mesh(0)
        ps.init()
        ps.register_point_cloud("Before cloud points", self.ms.mesh(len(self.ms)-1).vertex_matrix())
        ps.register_surface_mesh("Before Mesh", self.ms.mesh(len(self.ms)-1).vertex_matrix(), self.ms.mesh(len(self.ms)-1).face_matrix())
        ps.register_point_cloud("After cloud points", self.ms.mesh(len(self.ms)-2).vertex_matrix())
        ps.register_surface_mesh("After Mesh", self.ms.mesh(len(self.ms)-2).vertex_matrix(), self.ms.mesh(len(self.ms)-2).face_matrix())
        ps.show()

    def saveMesh(self, path=None):
        extension = settings[settingsName.meshExtension.value]
        # Same path with output instead of dbPath
        newPath = os.path.join(os.path.realpath(settings[settingsName.outputDBPath.value]),
                               os.path.relpath(self.meshPath, settings[settingsName.dbPath.value]))

        #Create parent dir if it doesn't exist
        os.makedirs(os.path.dirname(newPath), exist_ok=True)

        #Save the file in off format
        if path==None:
            self.ms.save_current_mesh(os.path.splitext(newPath)[0]+"."+extension)
        else:
            self.ms.save_current_mesh(path+"."+extension)

    def render(self):
        psUI.setPolyscopeSetting(1280, 720)
        ps.init()
        ps_cloud = ps.register_point_cloud("my points", self.ms.mesh(0).vertex_matrix())
        ps_cloud.set_radius(0.002)
        ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix())
        ps.show()


    def screenshot(self,saveTo, fileName=None):
        camLocation = settings[settingsName.screenPOV.value]
        os.makedirs('./screenshot', exist_ok=True)
        if fileName is None: fileName = os.path.splitext(os.path.basename(self.meshPath))[0]
        psUI.setPolyscopeSetting(450, 450)
        ps.init()
        ps.set_ground_plane_mode("none")
        ps.register_surface_mesh("my mesh", self.ms.mesh(0).vertex_matrix(), self.ms.mesh(0).face_matrix(), material='clay',color=[0,0,1])
        ps.set_screenshot_extension(".jpg");
        ps.set_up_dir("z_up")
        if camLocation == "diagonal" :
            ps.set_view_projection_mode('perspective')
            ps.look_at((1.5, -1.5 , 1.5), (0., 0., 0.))
        if camLocation == "straight" :
            ps.set_view_projection_mode('orthographic')
            ps.look_at((0., -0.5 , 0.), (0., 0., 0.))
        ps.screenshot(os.path.join(saveTo,fileName+'.jpg'), False)