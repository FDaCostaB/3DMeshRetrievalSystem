import render as rd
import sys
import data

features = data.exportMeshesData()
data.plotFeatures(features,['Category'],26,25,10)
data.plotFeatures(features,['Face numbers', 'Vertex numbers', 'Bounding Box Diagonal Size'])

#if (len(sys.argv) == 2):
#    print("Rendering : " + sys.argv[1])
#    rd.render(sys.argv[1])