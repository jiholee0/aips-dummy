from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TypeInfo(BaseModel):
    model_type: Optional[int] = Field(None, description="모델 타입 (예: 0 = GNN, 1 = ML, 2 = NLP)")
    chemical_type: Optional[int] = Field(None, description="화학 타입 (0: general 등)")

class PredictResult(BaseModel):
    prediction: Dict[str, Any] = Field(..., description="모델 예측 결과")
    summary: str = Field(..., description="LLM 기반 요약")

class JobStatusResponse(BaseModel):
    status: str = Field(..., description="작업 상태: processing | done | failed")
    result: Optional[PredictResult] = Field(None, description="작업 완료 시 결과 포함")

class PredictEnqueueResponse(BaseModel):
    job_id: str = Field(..., description="요청된 작업의 job_id")
