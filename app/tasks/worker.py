from app.services.model_caller import ModelCaller
from app.services.llm_caller import LLMCaller
from app.schemas.input_schema import InputSchema
from app.schemas.output_schema import PredictResult
from app.utils.redis_conn import redis_client
import json

def run_prediction_job(job_id: str, model_type: str, input_data: dict):
    from app.utils.logger import get_logger
    logger = get_logger(__name__)

    logger.info(f"[WORKER] 예측 job 실행: job_id={job_id}")

    input_obj = InputSchema(**input_data)

    properties = ["melting_point", "boiling_point", "vapor_pressure", "density", "solubility"]
    results = {}

    for prop in properties:
        try:
            result = ModelCaller.dummy_call(property_name=prop, model_type=model_type, data=input_obj)
            results[prop] = result
        except Exception as e:
            results[prop] = {"error": str(e)}

    summary = LLMCaller.dummy_summarize(results)

    result_obj = PredictResult(prediction=results, summary=summary)

    redis_key = f"result:{job_id}"
    redis_client.hset(redis_key, mapping={
        "status": "done",
        "result": result_obj.json()
    })

    logger.info(f"[WORKER] job_id={job_id} 처리 완료")
