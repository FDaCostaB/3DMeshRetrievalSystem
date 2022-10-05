import pymeshlab
import os


pricetonPath = "./Models/PRINCETON/test"
LabeledPath = r"D:\My Projects\UU\LabeledDB_new"

beforeRemesh = []
afterRemesh = []
nErrors = 0

for dir in os.scandir(LabeledPath):
    print(dir.name)
    FileIt =os.scandir(dir)
    for file in FileIt:
        rPath = os.path.realpath(file)
        print (file.name)
        fName = file.name.split(".")
        if len(fName) > 1:
            if fName[1] == "off":
                ms = pymeshlab.MeshSet()
                ms.load_new_mesh(rPath)
                cur = ms.current_mesh()
                print("Face number:" + str(cur.face_number()) + " - Vertex number:" + str(cur.vertex_number()))
                beforeRemesh.append(cur.vertex_number())
                try:
                    ms.compute_iso_parametrization()
                    ms.generate_iso_parametrization_remeshing(samplingrate = 5)
                    cur = ms.current_mesh()
                    print("Face number:" + str(cur.face_number()) + " - Vertex number:" + str(cur.vertex_number()))
                    afterRemesh.append(cur.vertex_number())
                except:
                    nErrors += 1
                    afterRemesh.append("Error")

print (beforeRemesh)
print (afterRemesh)
print ("Number of errors:" + str(nErrors))