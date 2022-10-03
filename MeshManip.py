import os.path
import pymeshlab
import polyscope as ps
import data

def refactor(meshPath, outputDir, ms, goal=10000, eps=1000):
    ms.load_new_mesh(meshPath)

    stats = data.dataMeshFilter(ms.current_mesh())

    print(stats)
    ms.apply_filter('meshing_remove_duplicate_faces')
    ms.apply_filter('meshing_remove_duplicate_vertices')
    ms.apply_filter('meshing_remove_unreferenced_vertices')
    # ms.apply_filter('generate_splitting_by_connected_components', delete_source_mesh=True)
    try :
        # ms.apply_filter('generate_resampled_uniform_mesh', cellsize=pymeshlab.Percentage(1))
        ms.apply_filter('compute_iso_parametrization')
        ms.apply_filter('generate_iso_parametrization_remeshing', samplingrate=7)
    except :
        refine(meshPath, outputDir, ms)
    stats = data.dataMeshFilter(ms.current_mesh())
    print(stats)

    ms.set_current_mesh(0)
    ms.save_current_mesh(os.path.join(outputDir,os.path.splitext(os.path.relpath(meshPath,'./Models'))[0]+".off"))

    ms.show_polyscope()
    ms.clear()


def refine(meshPath, outputDir,ms, goal=10000, eps=1000):
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

def compare(originalMeshPath,ms):
    ms.load_new_mesh(originalMeshPath)
    ps.init()
    ps.register_point_cloud("Before cloud points", ms.mesh(1).vertex_matrix())
    ps.register_surface_mesh("Before Mesh", ms.mesh(1).vertex_matrix(), ms.mesh(1).face_matrix())
    ps.register_point_cloud("After cloud points", ms.mesh(0).vertex_matrix())
    ps.register_surface_mesh("After Mesh", ms.mesh(0).vertex_matrix(), ms.mesh(0).face_matrix())
    ps.show()
    ms.clear()
