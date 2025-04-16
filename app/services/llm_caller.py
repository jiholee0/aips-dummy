import httpx
from app.core.config import LLM_ENDPOINT

class LLMCaller:

    @staticmethod
    def dummy_summarize(prediction_result: dict) -> str:
        # 간단한 요약문 생성 로직 (예시용)
        properties = [k for k, v in prediction_result.items() if v.get("confidence") in {"Good", "Moderate"}]
        
        if not properties:
            return "예측 결과에 신뢰할 수 있는 물성이 없어 요약을 생략합니다."

        example_lines = [f"{prop.replace('_', ' ')}에 대해 예측된 값은 {prediction_result[prop]['prediction']}입니다."
                         for prop in properties]

        summary = " ".join(example_lines[:3]) + " 이 화합물은 전반적으로 안정적인 특성을 가질 것으로 예상됩니다."
        return summary
    
    @staticmethod
    def summarize(prediction_result: dict) -> str:
        prompt = LLMCaller._build_prompt(prediction_result)

        try:
            response = httpx.post(LLM_ENDPOINT, json={"prompt": prompt}, timeout=30.0)
            response.raise_for_status()
            return response.json().get("summary", "요약 실패")
        except httpx.RequestError as e:
            raise RuntimeError(f"Request error when calling LLM endpoint: {e}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"HTTP error from LLM endpoint: {e.response.status_code} - {e.response.text}")

    @staticmethod
    def _build_prompt(prediction_result: dict) -> str:
        return f"""
        다음 input_json 데이터를 기반으로 물성 예측 요약문을 작성해줘. 요약문은 사용자에게 친절하고 이해하기 쉬운 문장으로 작성하며, 다음의 조건을 지켜줘:
        1. 각 물성(property)에 대해 예측값이 존재할 경우, 해당 값을 기반으로 화합물의 특성을 서술해줘.
        2. 신뢰도가 Moderate 또는 Good일 경우만 요약에 포함해. 그렇지 않거나 null이면 언급하지 않아도 돼.
        3. 예측값이 null이거나, "비고"에 "출력생략" 등의 지시가 있는 경우에는 해당 항목은 "출력을 생략했다"는 식으로 자연스럽게 설명해줘.
        4. 녹는점의 경우, 상온(25\u00b0C)과 비교하여 고체/액체 여부를 서술해줘.
        5. 증기압은 휘발성과 관련해 간단히 언급해줘.
        6. 요약은 2~4문장으로 간결하게 작성해줘.

        input_json:
        {prediction_result}
        """