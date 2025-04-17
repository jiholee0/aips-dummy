from fastapi import APIRouter, HTTPException
from app.utils.redis_conn import redis_client, rq_queue
from app.tasks.worker import run_prediction_job

admin_router = APIRouter()
REDIS_RESULT_PREFIX = "result:"

@admin_router.get("/queue-status", summary="RQ 큐 상태 조회", description="RQ에 대기 중인 job 목록과 개수를 조회합니다.")
def get_queue_status():
    jobs = rq_queue.jobs
    return {
        "total_pending_jobs": len(jobs),
        "job_ids": [job.id for job in jobs]
    }

@admin_router.post("/run-now/{job_id}", summary="job 강제 실행", description="특정 job_id와 임의 파라미터로 worker 작업을 즉시 실행합니다 (테스트용).")
def run_now(job_id: str):
    dummy_input = {
        "input_type": "smiles",
        "content": b"CCO"  # 임의 입력값
    }
    try:
        run_prediction_job(job_id=job_id, model_type="gnn", input_data=dummy_input)
        return {"message": f"Job {job_id} 강제 실행 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@admin_router.post("/reset-store", summary="Redis 저장소 초기화", description="Redis에 저장된 예측 결과를 모두 삭제합니다.")
def reset_store():
    keys = redis_client.keys(f"{REDIS_RESULT_PREFIX}*")
    if keys:
        redis_client.delete(*keys)
    return {"message": f"총 {len(keys)}개의 결과 삭제 완료"}


@admin_router.get("/store-status", summary="Redis 저장소 상태 조회", description="Redis에 저장된 예측 결과들의 상태를 조회합니다.")
def get_store_status():
    cursor = 0
    keys = []

    try:
        while True:
            cursor, batch = redis_client.scan(cursor=cursor, match=f"{REDIS_RESULT_PREFIX}*", count=100)
            keys.extend(batch)
            if cursor == 0:
                break
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis SCAN 실패: {str(e)}")

    if not keys:
        raise HTTPException(status_code=500, detail="저장된 예측 결과가 없습니다.")

    store_data = {}
    for key in keys:
        job_id = key.replace(REDIS_RESULT_PREFIX, "")
        job_data = redis_client.hgetall(key)
        store_data[job_id] = job_data

    return {
        "total_items": len(keys),
        "items": store_data
    }