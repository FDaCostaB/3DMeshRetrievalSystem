from enum import Enum

class dataName(Enum):
    CATEGORY = "Category"
    FACE_NUMBERS = "Face numbers"
    VERTEX_NUMBERS = "Vertex numbers"
    SIDE_SIZE = "Size of biggest bounding box side"
    MOMENT = "Moment order"
    SIZE = "Size"
    BARYCENTER = "Barycenter of the cloud points"
    DIST_BARYCENTER = "Distance of barycenter from origin"
    PCA = "PCA"
    DIAGONAL = "PymeshLab Diag"
    COMPONENTS_NUMBER = "Components number"


dataDimension = { dataName.CATEGORY: 1, dataName.FACE_NUMBERS : 1, dataName.VERTEX_NUMBERS : 1, dataName.SIDE_SIZE : 1,
                 dataName.MOMENT : 3, dataName.SIZE : 3, dataName.BARYCENTER : 3, dataName.DIST_BARYCENTER : 1, dataName.PCA : 3,
                  dataName.DIAGONAL : 1, dataName.COMPONENTS_NUMBER : 1 }