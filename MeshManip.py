import os.path
import pymeshlab
import polyscope as ps
import data
import numpy as np

def resample(meshPath, outputDir, ms, goal=10000, eps=1000):
    ms.load_new_mesh(meshPath)

    stats = data.dataMeshFilter(ms.current_mesh())

    print(stats)
    ms.apply_filter('meshing_remove_duplicate_faces')
    ms.apply_filter('meshing_remove_duplicate_vertices')
    ms.apply_filter('meshing_remove_unreferenced_vertices')
    ms.apply_filter('meshing_re_orient_faces_coherentely')
    # ms.apply_filter('generate_splitting_by_connected_components', delete_source_mesh=True)
    # ms.apply_filter('generate_resampled_uniform_mesh', cellsize=pymeshlab.Percentage(1))
    try :
        ms.apply_filter('compute_iso_parametrization')
        ms.apply_filter('generate_iso_parametrization_remeshing', samplingrate=7)
    except :
        refine(meshPath, ms)
    stats = data.dataMeshFilter(ms.current_mesh())
    print(stats)

    # normalise(meshPath,ms)

    ms.set_current_mesh(0)
    ms.save_current_mesh(os.path.join(outputDir,os.path.splitext(os.path.relpath(meshPath,'./Models'))[0]+".off"))

    ms.clear()


def refine(meshPath,ms, goal=10000, eps=1000):
    LIMIT = 5
    ms.load_new_mesh(meshPath)

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
            ms.apply_filter('meshing_decimation_quadric_edge_collapse', targetperc=0.8)
        stats = data.dataMeshFilter(ms.current_mesh())
        i+=1
    if(i==LIMIT):
        print("LIMIT reached")
        print(stats)
        print(meshPath)
        compare(meshPath,ms)

def compare(originalMeshPath,ms):
    ms.load_new_mesh(originalMeshPath)
    ps.init()
    ps.register_point_cloud("After cloud points", ms.mesh(1).vertex_matrix())
    ps.register_surface_mesh("After Mesh", ms.mesh(1).vertex_matrix(), ms.mesh(1).face_matrix())
    ps.register_point_cloud("Before cloud points", ms.mesh(0).vertex_matrix())
    ps.register_surface_mesh("Before Mesh", ms.mesh(0).vertex_matrix(), ms.mesh(0).face_matrix())
    ps.show()
    ms.clear()


def flipMomentTest(ms):
    moment=data.momentOrder(ms.current_mesh())
    ms.apply_matrix_flip_or_swap_axis(flipx=moment[0]<0,flipy=moment[1]<0,flipz=moment[2]<0)


def normalise(meshPath, ms, showDebug=False):
    ms.load_new_mesh(meshPath)

    out_dict = ms.get_geometric_measures()
    stats = data.dataMeshFilter(ms.current_mesh())
    print(stats)
    print('PCA')
    print(out_dict['pca'])
    print('Shell Barycenter')
    print(out_dict['shell_barycenter'])

    ms.compute_matrix_by_principal_axis()
    ms.apply_matrix_flip_or_swap_axis()
    out_dict = ms.get_geometric_measures()
    ms.compute_matrix_from_translation(traslmethod='XYZ translation', axisx=-1*out_dict['shell_barycenter'][0], axisy=-1*out_dict['shell_barycenter'][1], axisz=-1*out_dict['shell_barycenter'][2])
    ms.compute_matrix_from_scaling_or_normalization(customcenter=out_dict['shell_barycenter'], unitflag=True)
    flipMomentTest(ms)

    out_dict = ms.get_geometric_measures()
    stats = data.dataMeshFilter(ms.current_mesh())
    print(stats)
    print('PCA')
    print(out_dict['pca'])
    print('Shell Barycenter')
    print(out_dict['shell_barycenter'])

    if showDebug : compare(meshPath,ms)