import pymeshlab
import os
import pandas as pd

pricetonPath = "./Models/PRINCETON/test"
labeledPath = r"D:\My Projects\UU\LabeledDB_new"
# labeledPath = r"D:\My Projects\UU\Remeshed"
# labeledPath = r"D:\My Projects\UU\Remeshed10"
# remeshedDf = pd.read_csv(os.path.join(OutPath,"nVertices.csv"))

for dir in os.scandir(labeledPath):
    # if (dir.name == remeshedDf["class"]).any():
        # continue
    if not os.path.isdir(os.path.join(labeledPath,dir.name)):
        continue
    FileIt =os.scandir(dir)
    for file in FileIt:
        rPath = os.path.realpath(file)
        fName = file.name.split(".")
        if len(fName) > 1:
            if fName[1] == "off":
                ms = pymeshlab.MeshSet()
                ms.load_new_mesh(rPath)
                cur = ms.current_mesh()
                nOfVertices = cur.vertex_number()
                df = pd.DataFrame([[dir.name, file.name, nOfVertices]],columns=["class","fileName","nOfVertices"])
                df.to_csv(os.path.join(labeledPath,"nVertices.csv"),mode='a',header=False)
                ms.clear()