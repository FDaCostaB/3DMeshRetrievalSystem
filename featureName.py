from enum import Enum
from math import pi

class featureName(Enum):
    FILENAME = "File name"
    DIRNAME = "Folder name"
    A3 = "A3"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"
    SURFACE_AREA = "Surface area"
    VOLUME = "Volume"
    COMPACTNESS = "Compactness"
    SPHERICITY = "Sphericity"
    RECTANGULARITY = "Rectangularity"
    DIAMETER = "Diameter"
    ECCENTRICITY = "Eccentricity"
    CENTROID = "Centroid"


featureDimension = { featureName.A3.value: 1, featureName.D1.value : 0, featureName.D2.value : 1, featureName.D3.value : 1,
                     featureName.D4.value : 1, featureName.SURFACE_AREA.value : 1, featureName.VOLUME.value : 1,
                     featureName.COMPACTNESS.value : 1, featureName.SPHERICITY.value : 1, featureName.RECTANGULARITY.value : 1,
                     featureName.DIAMETER.value : 1, featureName.ECCENTRICITY.value : 1, featureName.CENTROID.value : 1 }

featureHistoBins = {}

histoUpperBound = { featureName.A3.value : pi, featureName.D1.value : 3**(1/2)/2, featureName.D2.value : 3**(1/2),
                     featureName.D3.value : (3/4)**(1/2), featureName.D4.value : (1/6)**(1/3) }

featureWeight = { featureName.A3.value: 2, featureName.D1.value : 0.5, featureName.D2.value : 2, featureName.D3.value : 2,
                     featureName.D4.value : 2, featureName.SURFACE_AREA.value : 2, featureName.VOLUME.value : 2,
                     featureName.COMPACTNESS.value : 3, featureName.SPHERICITY.value : 3, featureName.RECTANGULARITY.value : 3,
                     featureName.DIAMETER.value : 3, featureName.ECCENTRICITY.value : 3, featureName.CENTROID.value : 0.5 }