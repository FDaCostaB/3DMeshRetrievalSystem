import MeshManip
import render as rd
import sys
import data
import pymeshlab


if (len(sys.argv) == 2):
    print("Rendering : " + sys.argv[1])
    rd.render(sys.argv[1])
    #ms = pymeshlab.MeshSet()
    #MeshManip.refine(sys.argv[1],'./output',ms,10000,1000)
else :
    data.normaliseVertex(5000,1000)
    #features = data.exportMeshesData()
    #data.plotFeatures(features, ['Category'], 26, 25, 10)
    #data.plotFeatures(features, ['Face numbers', 'Vertex numbers', 'Bounding Box Diagonal Size'])