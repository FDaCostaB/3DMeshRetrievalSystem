import pymeshlab
import polyscope as ps

def render(s):
    ms = pymeshlab.MeshSet()

    ms.load_new_mesh(s)

    ps.init()
    ps.register_point_cloud("my points", ms.mesh(0).vertex_matrix())
    ps.register_surface_mesh("my mesh", ms.mesh(0).vertex_matrix(), ms.mesh(0).face_matrix())
    ps.show()

