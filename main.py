import MeshManip
import render as rd
import sys
import data
import pymeshlab


if (len(sys.argv) == 2):
    ms = pymeshlab.MeshSet()
    # MeshManip.normalise(sys.argv[1], ms, True)
    MeshManip.resample(sys.argv[1], './output', ms, 10000, 1000)
else :
    data.normaliseVertex(10000,1000)
    features = data.exportMeshesData('Models')
    data.plotFeatures(features, ['Category'], 26, 25, 10,'Models')
    data.plotFeatures(features, ['Face numbers', 'Vertex numbers', 'Bounding Box Diagonal Size'],'Models')
    features = data.exportMeshesData('output')
    data.plotFeatures(features, ['Category'], 26, 25, 10,'output')
    data.plotFeatures(features, ['Face numbers', 'Vertex numbers', 'Bounding Box Diagonal Size'],'output')
