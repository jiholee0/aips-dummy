from fastapi import APIRouter
from app.router.model_router import FAKE_RESULT_STORE  # 또는 서비스/스토리지에서 import

admin_router = APIRouter()

@admin_router.post("/reset-store", summary="더미 데이터 초기화", description="FAKE_RESULT_STORE를 초기화합니다.")
def reset_store():
    FAKE_RESULT_STORE.clear()
    return {"message": "FAKE_RESULT_STORE 초기화 완료"}
