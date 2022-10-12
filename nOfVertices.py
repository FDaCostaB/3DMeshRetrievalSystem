import pymeshlab
import os
import pandas as pd

pricetonPath = "./Models/PRINCETON/test"
labeledPath = r"D:\My Projects\UU\LabeledDB_new"
labeledPath = r"D:\My Projects\UU\RemeshedLabeledDB"
# labeledPath = r"D:\My Projects\UU\RemeshedPrinceton"
# labeledPath = r"D:\My Projects\UU\Remeshed"
# labeledPath = r"D:\My Projects\UU\Remeshed10"
# remeshedDf = pd.read_csv(os.path.join(OutPath,"nVertices.csv"))

nOfVertices = []
classes = []
names = []
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
            if fName[1] == "off" or fName[1] == "ply":
                ms = pymeshlab.MeshSet()
                ms.load_new_mesh(rPath)
                cur = ms.current_mesh()
                classes.append(dir.name)
                names.append(fName[0])
                nOfVertices.append(cur.vertex_number())
                ms.clear()

                
df = pd.DataFrame({"class":classes, "name":names, "nOfVertices":nOfVertices},columns=["class","name","nOfVertices"])
df.to_csv(os.path.join(labeledPath,"nVertices.csv"))