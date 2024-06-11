from fastapi import APIRouter


router = APIRouter()

@router.get("/board")
def get_test_code():
    return {"respose": 200}