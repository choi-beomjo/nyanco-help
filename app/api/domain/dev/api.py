from fastapi import APIRouter, Depends
from redis import Redis
from ...deps import get_redis
from ...tags import Tags

router = APIRouter(tags=[Tags.dev])


@router.get("/redis-health")
def health_check(redis: Redis = Depends(get_redis)):
    try:
        redis.ping()
        return {"redis": "ok"}
    except Exception as e:
        return {"redis": f"error: {str(e)}"}