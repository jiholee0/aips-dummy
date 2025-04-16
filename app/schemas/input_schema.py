from pydantic import BaseModel, Field
from typing import Literal

class InputSchema(BaseModel):
    input_type: Literal['mol', 'smiles', 'mol_3d'] = Field(..., description="입력 데이터 타입")
    content: bytes = Field(..., description="화학 구조 파일 내용")
