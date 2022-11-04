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


featureWeight = { featureName.A3.value: -10.0, featureName.D1.value : 8.75, featureName.D2.value : -10.0, featureName.D3.value : -10.0,
                     featureName.D4.value : -10.0, featureName.SURFACE_AREA.value : 10.0, featureName.VOLUME.value : 10.0,
                     featureName.COMPACTNESS.value : -0.78, featureName.SPHERICITY.value : -8.76, featureName.RECTANGULARITY.value : -10.0,
                     featureName.DIAMETER.value : -1.73, featureName.ECCENTRICITY.value : 0.50, featureName.CENTROID.value : 0.89 }

featureDimension = { featureName.A3.value: 2, featureName.D1.value : 2, featureName.D2.value : 2, featureName.D3.value : 2,
                     featureName.D4.value : 2, featureName.SURFACE_AREA.value : 1, featureName.VOLUME.value : 1,
                     featureName.COMPACTNESS.value : 1, featureName.SPHERICITY.value : 1, featureName.RECTANGULARITY.value : 1,
                     featureName.DIAMETER.value : 1, featureName.ECCENTRICITY.value : 1, featureName.CENTROID.value : 1 }

featureHistoBins = {}

histoUpperBound = { featureName.A3.value : pi, featureName.D1.value : 3**(1/2)/2, featureName.D2.value : 3**(1/2),
                     featureName.D3.value : (3/4)**(1/2), featureName.D4.value : (1/6)**(1/3) }
