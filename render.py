import pymeshlab
import polyscope as ps

def render(s):
    # We can load meshes from a file by specifying its path or by explicitely
    # giving the vertices and the normals of the mesh you want to render
    ms = pymeshlab.MeshSet()

    ms.load_new_mesh(s)

    #pymesh function to dispaly mesh in a polyscope windows
    # ms.show_polyscope()

    #Using polyscope function to have more control on the view
    # Initialize polyscope
    ps.init()

    ps.register_point_cloud("my points", ms.mesh(0).vertex_matrix())
    ps.register_surface_mesh("my mesh", ms.mesh(0).vertex_matrix(), ms.mesh(0).face_matrix())#, smooth_shade=True)
    ps.show()

#    ms.generate_convex_hull()
#    ms.save_current_mesh('convex_hull.ply')
    out_dict = ms.get_geometric_measures()
    print(out_dict['surface_area'])