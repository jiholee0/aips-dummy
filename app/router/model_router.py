import random
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.input_schema import InputSchema
from app.schemas.output_schema import PredictResult, PredictEnqueueResponse, JobStatusResponse
from app.services.interpreter import Interpreter
from app.services.model_caller import ModelCaller
from app.services.llm_caller import LLMCaller
from app.utils.model_enum import ModelType
from app.utils.logger import get_logger
from app.utils.redis_conn import redis_client, rq_queue
import uuid

model_router = APIRouter()
logger = get_logger(__name__)

# 예시 메모리 기반 저장소 (실제 서비스 시 DB로 교체 필요)
FAKE_RESULT_STORE = {}

# 예측 결과를 저장하고 조회하는 Redis 키 접두어
REDIS_PREFIX = "predict_job:"

@model_router.post("/predict", response_model=PredictEnqueueResponse, status_code=202, summary="예측 요청", description="파일을 업로드하여 예측을 요청합니다.")
async def enqueue_prediction(file: UploadFile = File(...)): # 비동기 파일 업로드
    logger.info("/predict 요청 수신")

    content = await file.read()
    interpretation = Interpreter.interpret(content)

    if not interpretation["valid"]:
        raise HTTPException(status_code=400, detail=interpretation["reason"])

    input_type = interpretation["type"]["input_type"]
    model_type = interpretation["type"]["model_type"]
    logger.info(f"입력 타입: {input_type}, 모델 타입: {model_type}")

    input_data = InputSchema(input_type=input_type, content=content)

    job_id = str(uuid.uuid4())
    logger.info(f"job_id 생성: {job_id}")

    # RQ Queue에 Job 등록
    rq_queue.enqueue(
        "app.tasks.worker.run_prediction_job",
        job_id=job_id,
        model_type=model_type,
        input_data=input_data.dict()
    )

    # 초기 상태 Redis에 저장
    redis_client.hset(f"{REDIS_PREFIX}{job_id}", mapping={
        "status": "processing",
        "result": ""
    })

    return {"job_id": job_id}

    # # 예측 대상 property 리스트
    # properties = ["melting_point", "boiling_point", "vapor_pressure", "density", "solubility"]

    # results = {}
    # for prop in properties:
    #     try:
    #         result = ModelCaller.dummy_call(property_name=prop, model_type=model_type, data=input_data)
    #         results[prop] = result
    #     except Exception as e:
    #         logger.error(f"{prop} 예측 실패: {e}")
    #         results[prop] = {"error": str(e)}

    # summary = LLMCaller.dummy_summarize(results)

    # result_obj = PredictResult(
    #     prediction=results,
    #     summary=summary
    # )

    # job_id = str(uuid.uuid4())
    
    # # 50% 확률로 processing 상태 저장
    # job_status = "processing" if random.random() < 0.5 else "done"
    # FAKE_RESULT_STORE[job_id] = {
    #     "status": job_status,
    #     "result": result_obj if job_status == "done" else None
    # }

    # logger.info(f"결과 저장 완료: job_id={job_id}")

    # return {"job_id": job_id}


@model_router.get("/result/{job_id}", response_model=JobStatusResponse, summary="예측 결과 조회", description="예측 결과를 조회합니다.")
def get_result(job_id: str):
    logger.info(f"/result 조회 요청: job_id={job_id}")
    redis_key = f"{REDIS_PREFIX}{job_id}"
    job_data = redis_client.hgetall(redis_key)

    if not job_data:
        logger.warning("결과 없음")
        raise HTTPException(status_code=404, detail="Job not found")
    
    result_json = job_data.get("result")
    logger.info(f"결과 상태: {job_data['status']}")
    return {
        "status": job_data.get("status"),
        "result": PredictResult.parse_raw(result_json) if result_json else None
    }
