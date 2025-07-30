from fastapi import APIRouter, Depends
from redis import Redis
from ...deps import get_redis, get_current_user
from ...tags import Tags
from ...domain.user.schemas import User
from fastapi.responses import JSONResponse

router = APIRouter(tags=[Tags.dev])


@router.get("/redis-health")
def health_check(redis: Redis = Depends(get_redis)):
    try:
        redis.ping()
        return {"redis": "ok"}
    except Exception as e:
        return {"redis": f"error: {str(e)}"}


@router.get("/token/check")
def check_token(user: User = Depends(get_current_user)):
    return JSONResponse(status_code=200, content={"message": "Token is valid", "username": user.name})