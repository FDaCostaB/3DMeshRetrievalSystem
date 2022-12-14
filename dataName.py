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
    EIGENVALUES = "Eigenvalues"


dataDimension = { dataName.CATEGORY.value: 1, dataName.FACE_NUMBERS.value : 1, dataName.VERTEX_NUMBERS.value : 1,
                  dataName.SIDE_SIZE.value : 1, dataName.MOMENT.value : 3, dataName.SIZE.value : 3,
                  dataName.BARYCENTER.value : 3, dataName.DIST_BARYCENTER.value : 1, dataName.PCA.value : 3,
                  dataName.DIAGONAL.value : 1, dataName.COMPONENTS_NUMBER.value : 1, dataName.EIGENVALUES.value : 3 }