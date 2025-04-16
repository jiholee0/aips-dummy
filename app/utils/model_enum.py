from enum import IntEnum

class ModelType(IntEnum):
    GNN = 0
    ML = 1
    NLP = 2
    # GNN_ML_ENSEMBLE = 3  # 향후 확장 가능

class ChemicalType(IntEnum):
    GENERAL = 0
    # 향후 1~5로 특성 기반 분류 확장 가능