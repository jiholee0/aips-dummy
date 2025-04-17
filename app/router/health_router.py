from fastapi import APIRouter, HTTPException
from app.utils.redis_conn import redis_client

health_router = APIRouter()

@health_router.get("/api", tags=["0. health"], summary="API 서버 헬스 체크", description="FastAPI 서버가 정상 동작하는지 확인합니다.")
def health_check_api():
    return {"message": "API is running."}


@health_router.get("/redis", tags=["0. health"], summary="Redis 연결 상태 체크", description="Redis 서버와의 연결 상태를 확인합니다.")
def health_check_redis():
    try:
        pong = redis_client.ping()
        if pong:
            return {"redis": "connected"}
        else:
            raise Exception("No PONG received")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis 연결 실패: {str(e)}")
