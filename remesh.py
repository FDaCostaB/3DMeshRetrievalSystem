import pymeshlab
import os
import pandas as pd

pricetonPath = "./Models/PRINCETON/test"
# LabeledPath = r"D:\My Projects\UU\LabeledDB_new"
labeledPath = r"D:\My Projects\UU\Remeshed"
OutPath = r"D:\My Projects\UU\Remeshed10"
remeshedDf = pd.read_csv(os.path.join(OutPath,"nVertices.csv"))

for dir in os.scandir(labeledPath):
    if (dir.name == remeshedDf["class"]).any():
        continue
    curPath = os.path.join(OutPath,dir.name)
    if not os.path.isdir(os.path.join(labeledPath,dir.name)):
        continue
    os.mkdir(curPath)
    FileIt =os.scandir(dir)
    for file in FileIt:
        rPath = os.path.realpath(file)
        fName = file.name.split(".")
        if len(fName) > 1:
            if fName[1] == "off":
                ms = pymeshlab.MeshSet()
                ms.load_new_mesh(rPath)
                cur = ms.current_mesh()
                beforeRemeshVerices = cur.vertex_number()
                try:
                    ms.apply_filter('meshing_remove_duplicate_faces')
                    ms.apply_filter('meshing_remove_duplicate_vertices')
                    ms.apply_filter('meshing_remove_unreferenced_vertices')
                    try :
                        ms.apply_filter('meshing_repair_non_manifold_edges', method='Split Vertices')
                        ms.apply_filter('meshing_repair_non_manifold_vertices')
                        ms.apply_filter('meshing_re_orient_faces_coherentely')
                    except:
                        print('ERROR : Mesh has some not 2-manifold faces')
                    ms.compute_iso_parametrization()
                    ms.generate_iso_parametrization_remeshing(samplingrate = 10)
                    cur = ms.current_mesh()
                    afterRemeshVerices = cur.vertex_number()
                    ms.save_current_mesh(os.path.join(curPath, file.name))
                except:
                    afterRemeshVerices = "Error"
                df = pd.DataFrame([[dir.name, file.name, beforeRemeshVerices, afterRemeshVerices]],columns=["class","fileName","beforeRemesh","afterRemesh"])
                df.to_csv(os.path.join(OutPath,"nVertices.csv"),mode='a',header=False)
                ms.clear()