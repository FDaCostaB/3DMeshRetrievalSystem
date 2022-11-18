import os.path
from enum import Enum
from featureName import featureHistoBins, featureName

settings = {}

class settingsName(Enum):
    dbPath = "DATABASE FOLDER PATH"
    outputPath = "OUTPUT FOLDER PATH"
    outputDBPath = "OUTPUT DB PATH"
    meshExtension = "3D MESH EXTENSION"
    imageExtension = "IMAGE MESH EXTENSION"
    expectedVerts = "EXPECTED NUMBERS OF VERTICES"
    epsVerts = "NB OF VERTICES EPSILON"
    nbBinsData = "NB OF BINS DATA HISTOGRAM"
    binsA3 = "NB OF BINS A3"
    binsD1 = "NB OF BINS D1"
    binsD2 = "NB OF BINS D2"
    binsD3 = "NB OF BINS D3"
    binsD4 = "NB OF BINS D4"
    nbSample = "NUMBER OF MEASURE FOR HISTOGRAM FEATURES"
    normType ="NORMALISATION TYPE"
    screenPOV = "POV SCREENSHOT"
    debug = "DEBUG"


def readSettings():
    f = open("settings.mr", "r")
    lines = f.readlines()
    for line in lines:
        if len(line) > 0 and line[0]!='#' and line[0]!='\n':
            name = line.split('=')[0]
            value = line.split('=')[1]
            if value[len(value)-1] == '\n':
                value = value[:len(value) - 1]
            if name=='DATABASE FOLDER PATH':
                settings[name] = value
            elif name=='OUTPUT FOLDER PATH':
                settings[name] = value
                settings[settingsName.outputDBPath.value] = os.path.join(value,'NormaliseDB')
            elif name=='3D MESH EXTENSION':
                settings[name] = "."+value.lower()
            elif name=='IMAGE MESH EXTENSION':
                settings[name] = "."+value.lower()
            elif name=='EXPECTED NUMBERS OF VERTICES':
                settings[name] = int(value)
            elif name=='NB OF VERTICES EPSILON':
                settings[name] = int(value)
            elif name=='NB OF BINS DATA HISTOGRAM':
                settings[name] = int(value)
            elif name=='NB OF BINS A3':
                featureHistoBins[featureName.A3.value] = int(value)
                settings[name] = int(value)
            elif name=='NB OF BINS D1':
                featureHistoBins[featureName.D1.value] = int(value)
                settings[name] = int(value)
            elif name=='NB OF BINS D2':
                featureHistoBins[featureName.D2.value] = int(value)
                settings[name] = int(value)
            elif name=='NB OF BINS D3':
                featureHistoBins[featureName.D3.value] = int(value)
                settings[name] = int(value)
            elif name=='NB OF BINS D4':
                featureHistoBins[featureName.D4.value] = int(value)
                settings[name] = int(value)
            elif name=='NUMBER OF MEASURE FOR HISTOGRAM FEATURES':
                settings[name] = int(value)
            elif name=='NORMALISATION TYPE':
                settings[name] = value
            elif name=='POV SCREENSHOT':
                settings[name] = value
            elif name=='DEBUG':
                if value.lower() == "false":
                    settings[name] = False
                elif value.lower() == "true":
                    settings[name] = True