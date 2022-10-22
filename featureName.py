from enum import Enum

class featureName(Enum):
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


featureDimension = { featureName.A3.value: 2, featureName.D1.value : 2, featureName.D2.value : 2, featureName.D3.value : 2,
                     featureName.D4.value : 2, featureName.SURFACE_AREA.value : 1, featureName.VOLUME.value : 1,
                     featureName.COMPACTNESS.value : 1, featureName.SPHERICITY.value : 1, featureName.RECTANGULARITY.value : 1,
                     featureName.DIAMETER.value : 1, featureName.ECCENTRICITY.value : 1, featureName.CENTROID.value : 1 }

featureHistoBins = { featureName.A3.value : 36, featureName.D1.value : 30, featureName.D2.value : 30,
                     featureName.D3.value : 30, featureName.D4.value : 30 }

featureWeight = { featureName.A3.value: 1, featureName.D1.value : 0.5, featureName.D2.value : 1, featureName.D3.value : 1,
                     featureName.D4.value : 1, featureName.SURFACE_AREA.value : 2, featureName.VOLUME.value : 2,
                     featureName.COMPACTNESS.value : 2, featureName.SPHERICITY.value : 2, featureName.RECTANGULARITY.value : 2,
                     featureName.DIAMETER.value : 2, featureName.ECCENTRICITY.value : 2, featureName.CENTROID.value : 0.5 }