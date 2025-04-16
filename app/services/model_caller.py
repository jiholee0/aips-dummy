import httpx
from app.schemas.input_schema import InputSchema
from app.core.config import MODEL_ENDPOINTS

class ModelCaller:

    @staticmethod
    def dummy_call(property_name: str, model_type: str, data: InputSchema) -> dict:
        # 더미 데이터 생성
        dummy_prediction = round(42.0 + hash(str(property_name) + str(model_type)) % 50, 2)
        dummy_result = {
            "prediction": dummy_prediction,
            "confidence": "Good" if dummy_prediction % 2 == 0 else "Moderate",
            "upper_bound": dummy_prediction + 5.0,
            "lower_bound": dummy_prediction - 5.0,
            "status": "정상"
        }

        return dummy_result
    
    @staticmethod
    def call(property_name: str, model_type: str, data: InputSchema) -> dict:
        
        url = MODEL_ENDPOINTS.get(property_name, {}).get(model_type)
        if not url:
            raise ValueError(f"Unsupported property/model combination: '{property_name}' / '{model_type}'")

        payload = {
            "input_type": data.input_type,
            "content": data.content
        }

        try:
            response = httpx.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            result = response.json()

            # 결과 필드 파싱
            prediction = result.get("prediction")
            confidence = result.get("confidence")
            upper_bound = result.get("upper_bound")
            lower_bound = result.get("lower_bound")
            status = result.get("status") or "None"

            if status == "선택생략" or prediction is None:
                return {
                    "prediction": None,
                    "confidence": None,
                    "upper_bound": None,
                    "lower_bound": None,
                    "status": "선택생략"
                }

            return {
                "prediction": prediction,
                "confidence": confidence,
                "upper_bound": upper_bound,
                "lower_bound": lower_bound,
                "status": status
            }

        except httpx.RequestError as e:
            raise RuntimeError(f"Request error when calling model endpoint: {e}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"HTTP error from model endpoint: {e.response.status_code} - {e.response.text}")
