import logging
import sys

# 로그 포맷 정의
log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# 루트 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log", encoding="utf-8")  # 파일로 저장
    ]
)

# 커스텀 로거 함수
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
