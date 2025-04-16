## 1. 서버 실행
```bash
uvicorn app.main:app --reload
```
- --reload : 코드 변경 시 자동으로 서버 재시작 (개발용)
- 기본 접속 주소 : http://127.0.0.1:8000

## 📘 Swagger 문서  
- 접속 주소 : http://127.0.0.1:8000/docs
- OpenAPI 명세 : http://127.0.0.1:8000/openapi.json

## 디렉토리 구조
```
apis-server/
├── app/
│   ├── main.py                      # FastAPI 엔트리포인트
│   ├── router/                      # FastAPI 라우터
│   │   ├── admin_router.py          # /admin
│   │   └── model_router.py          # /model
│   ├── services/                    # 비즈니스 로직
│   │   ├── interpreter.py           # 모델 선택/유효성 판단
│   │   ├── model_caller.py          # 모델 호출
│   │   └── llm_caller.py            # LLM 호출
│   ├── tasks/                       # RQ worker (추후 도입)
│   │   └── worker.py
│   ├── schemas/                     # Pydantic 정의
│   │   ├── input_schema.py
│   │   └── output_schema.py
│   ├── utils/                       # 공통 유틸
│   │   ├── logger.py
│   │   ├── model_enum.py
│   │   └── redis_conn.py
│   └── core/
│       └── config.py                # 환경변수, 엔드포인트 주소 등 설정
├── requirements.txt
├── README.md
└── Dockerfile
```
