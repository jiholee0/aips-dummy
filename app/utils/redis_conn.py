import redis
from rq import Queue

# Redis 연결 객체 (RQ 전용: decode_responses=False)
raw_redis_conn = redis.Redis(host="localhost", port=6380, db=0, decode_responses=False)

# 일반 문자열용 Redis (FastAPI용: decode_responses=True)
redis_client = redis.Redis(host="localhost", port=6380, db=0, decode_responses=True)

# RQ Queue는 raw 연결 사용
rq_queue = Queue('default', connection=raw_redis_conn)
