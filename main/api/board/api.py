from fastapi import APIRouter
from ..tags import Tags


router = APIRouter()

@router.get("/board", tags=[Tags.board])
def get_test_code():
    return {"respose": 200}