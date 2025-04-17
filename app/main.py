from fastapi import FastAPI
from app.router.admin_router import admin_router
from app.router.model_router import model_router
from app.router.health_router import health_router

tags_metadata = [
    {"name": "0. health", "description": "헬스 체크 및 시스템 상태 API"},
    {"name": "1. admin", "description": "관리자 기능 API"},
    {"name": "2. inference", "description": "모델 추론 API"}
]

app = FastAPI(title="Trand AI Dummy API", openapi_tags=tags_metadata)

# 라우터 등록
app.include_router(health_router, prefix="/health", tags=["0. health"])
app.include_router(admin_router, prefix="/admin", tags=["1. admin"])
app.include_router(model_router, prefix="/model", tags=["2. inference"])