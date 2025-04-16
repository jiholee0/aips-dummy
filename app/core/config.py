import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

# 모델 타입에 따른 Kubeflow 엔드포인트 정의
MODEL_ENDPOINTS = {
    "melting_point" : {
        0: os.getenv("GNN_MODEL_ENDPOINT", "http://localhost:8001/gnn/melting_point/predict"),
        1: os.getenv("ML_MODEL_ENDPOINT", "http://localhost:8002/ml/melting_point/predict"),
        2: os.getenv("NLP_MODEL_ENDPOINT", "http://localhost:8003/nlp/melting_point/predict"),
    },
    "boiling_point" : {
        0: os.getenv("GNN_MODEL_ENDPOINT", "http://localhost:8001/gnn/melting_point/predict"),
        1: os.getenv("ML_MODEL_ENDPOINT", "http://localhost:8002/ml/melting_point/predict"),
        2: os.getenv("NLP_MODEL_ENDPOINT", "http://localhost:8003/nlp/melting_point/predict"),
    },
}

# LLM 호출용 엔드포인트
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://localhost:9000/llm/summarize")