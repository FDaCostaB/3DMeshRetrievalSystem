import os.path
import pymeshlab
import polyscope as ps
import data
import numpy as np

def saveMesh(id,ms,meshPath, outputDir):
    ms.set_current_mesh(id)
    ms.save_current_mesh(os.path.join(outputDir,os.path.splitext(os.path.relpath(meshPath,'./Models'))[0]+".off"))


def resample(meshPath, outputDir, ms, goal=10000, eps=1000, showComparison=False):
    ms.load_new_mesh(meshPath)
    stats = data.dataMeshFilter(ms.current_mesh())
    if showComparison:
        print(stats)

    ms.apply_filter('meshing_remove_duplicate_faces')
    ms.apply_filter('meshing_remove_duplicate_vertices')
    ms.apply_filter('meshing_remove_unreferenced_vertices')
    try :
        ms.apply_filter('meshing_repair_non_manifold_edges', method='Split Vertices')
        ms.apply_filter('meshing_repair_non_manifold_vertices')
        ms.apply_filter('meshing_re_orient_faces_coherentely')
    except:
        print('ERROR : Mesh has some not 2-manifold faces ('+meshPath+')')
    refine(ms,meshPath,goal=goal,eps=eps)
    normalise(ms,meshPath)
    saveMesh(0,ms,meshPath,outputDir)

    stats = data.dataMeshFilter(ms.current_mesh())
    if showComparison:
        print(stats)
        compare(ms, meshPath)
    ms.clear()


def refine(ms,meshPath, goal=10000, eps=1000,reload=False):
    LIMIT = 5
    if(reload):ms.load_new_mesh(meshPath)

    stats = data.dataMeshFilter(ms.current_mesh())
    i=0
    while ( (stats["Vertex numbers"] < goal - eps or stats["Vertex numbers"] > goal + eps) and i<LIMIT):
        if (stats["Vertex numbers"] < goal - eps):
            try:
                ms.apply_filter('meshing_surface_subdivision_loop', iterations=1)
            except:
                ms.apply_filter('meshing_repair_non_manifold_edges', method='Remove Faces')
                ms.apply_filter('meshing_repair_non_manifold_vertices')
        elif (stats["Vertex numbers"] > goal + eps):
            ms.apply_filter('meshing_decimation_quadric_edge_collapse', targetperc=goal/stats["Vertex numbers"])
        stats = data.dataMeshFilter(ms.current_mesh())
        i+=1
    if(i==LIMIT):
        print("LIMIT reached")
        print(meshPath)
    ms.apply_filter('apply_coord_laplacian_smoothing',stepsmoothnum=3)


def compare(ms,originalMeshPath=None):
    if(originalMeshPath!=None):
        ms.load_new_mesh(originalMeshPath)
        beforeID=len(ms)-1
    ps.init()
    ps.register_point_cloud("Before cloud points", ms.mesh(beforeID).vertex_matrix())
    ps.register_surface_mesh("Before Mesh", ms.mesh(beforeID).vertex_matrix(), ms.mesh(beforeID).face_matrix())
    ps.register_point_cloud("After cloud points", ms.mesh(0).vertex_matrix())
    ps.register_surface_mesh("After Mesh", ms.mesh(0).vertex_matrix(), ms.mesh(0).face_matrix())
    ps.show()


def flipMomentTest(ms, debugLog = False):
    moment=data.momentOrder(ms.current_mesh())
    if(moment[0]<0 and debugLog ):print('Flip x axis')
    if(moment[1]<0 and debugLog ):print('Flip y axis')
    if(moment[2]<0 and debugLog ):print('Flip z axis')
    ms.apply_matrix_flip_or_swap_axis(flipx=moment[0]<0,flipy=moment[1]<0,flipz=moment[2]<0)


def normalise(ms,meshPath, showDebug =False,reload=False):
    if(reload): ms.load_new_mesh(meshPath)

    out_dict = ms.get_geometric_measures()
    if(showDebug):
        stats = data.dataMeshFilter(ms.current_mesh())
        print('Size :' + str(stats['Size']) + ', Shell Barycenter : ' +str(out_dict['shell_barycenter']) +', Moment order'+ str(np.sign(stats['Moment order'])))
        print('PCA :')
        print(out_dict['pca'])

    ms.compute_matrix_from_translation(traslmethod='XYZ translation', axisx=-1*out_dict['shell_barycenter'][0], axisy=-1*out_dict['shell_barycenter'][1], axisz=-1*out_dict['shell_barycenter'][2])
    ms.compute_matrix_by_principal_axis()
    ms.apply_matrix_flip_or_swap_axis(swapxz=True)
    ms.compute_matrix_from_scaling_or_normalization(customcenter=out_dict['shell_barycenter'], unitflag=True)
    flipMomentTest(ms, showDebug)

    if (showDebug):
        out_dict = ms.get_geometric_measures()
        stats = data.dataMeshFilter(ms.current_mesh())
        print('Size :' + str(stats['Size']) + ', Shell Barycenter : ' +str(out_dict['shell_barycenter']) +', Moment order'+ str(np.sign(stats['Moment order'])))
        print('PCA :')
        print(out_dict['pca'])
        compare(ms,meshPath)