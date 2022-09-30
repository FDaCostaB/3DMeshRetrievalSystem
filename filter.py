import pymeshlab
from pathlib import Path
import os
import math


def dataFilter(path):
    p1 = Path(path)
    category = os.path.relpath(p1.parent, p1.parent.parent)
    fileType = p1.suffix
    ms = pymeshlab.MeshSet()
    if(fileType == ".obj" or fileType == ".off"):
        ms.load_new_mesh(path)
        cur = ms.current_mesh()
        sizeFace = {}
        for face in cur.polygonal_face_list():
            if sizeFace.get(str(len(face))) is not None:
                sizeFace[str(len(face))] += 1
            else:
                sizeFace[str(len(face))] = 1
            if len(face)==4 : raise Exception("Quads found")
        diagSize = math.sqrt(cur.bounding_box().dim_x()+cur.bounding_box().dim_y()+cur.bounding_box().dim_z())
        res = {"Category" : category, "Face numbers" : cur.face_number(), "Vertex numbers" : cur.vertex_number(), "Bounding Box Diagonal Size" : diagSize, "Types of faces" : sizeFace}
        ms.clear()
        return res