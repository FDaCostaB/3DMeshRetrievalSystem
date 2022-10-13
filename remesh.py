import pymeshlab
import os
import pandas as pd

labeledPath = r"D:\My Projects\UU\PRINCETON"
labeledPath = r"D:\My Projects\UU\LabeledDB_new"
# labeledPath = r"D:\My Projects\UU\Remeshed"
OutPath = r"D:\My Projects\UU\RemeshedLabeledDB"
# OutPath = r"D:\My Projects\UU\RemeshedPrinceton"
# remeshedDf = pd.read_csv(os.path.join(OutPath,"nVertices.csv"))
if not os.path.exists(OutPath):
    os.mkdir(OutPath)

for dir in os.scandir(labeledPath):
    # if (dir.name == remeshedDf["class"]).any():
    #     continue
    curPath = os.path.join(OutPath,dir.name)
    if not os.path.isdir(os.path.join(labeledPath,dir.name)):
        continue
    if not os.path.exists(curPath):
        os.mkdir(curPath)
    FileIt =os.scandir(dir)
    for file in FileIt:
        if os.path.exists(os.path.join(curPath, file.name)):
            continue
        rPath = os.path.realpath(file)
        fName = file.name.split(".")
        if len(fName) > 1:
            if fName[1] == "off" or fName[1] == "ply":
                ms = pymeshlab.MeshSet()
                ms.load_new_mesh(rPath)
                cur = ms.current_mesh()
                beforeRemeshVerices = cur.vertex_number()
                try:
                    # ms.apply_filter('meshing_remove_duplicate_faces')
                    # ms.apply_filter('meshing_remove_duplicate_vertices')
                    # ms.apply_filter('meshing_remove_unreferenced_vertices')
                    # try :
                    #     ms.apply_filter('meshing_repair_non_manifold_edges', method='Split Vertices')
                    #     ms.apply_filter('meshing_repair_non_manifold_vertices')
                    #     ms.apply_filter('meshing_re_orient_faces_coherentely')
                    # except:
                    #     print('ERROR : Mesh has some not 2-manifold faces')
                    # ms.compute_iso_parametrization()
                    # ms.generate_iso_parametrization_remeshing(samplingrate = 5)
                    p0 = pymeshlab.Percentage(1.25)
                    p1 = pymeshlab.Percentage(0)
                    ms.generate_resampled_uniform_mesh(cellsize = p0)
                    ms.save_current_mesh(os.path.join(curPath, file.name))
                except Exception as e:
                    afterRemeshVerices = "Error"
                    print(str(e))
                ms.clear()