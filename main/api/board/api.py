from fastapi import APIRouter, Depends
from ..tags import Tags
from utils.msg.msg import Msg
from db.crud.crud import get_crud, CRUD
from .utils import *
from .models import *


router = APIRouter(tags=[Tags.board])

@router.get("/board")
def get_test_code(crud: CRUD = Depends(get_crud)):
    return Msg(msg="success")


@router.post("/post")
def add_post(post: Post,crud: CRUD = Depends(get_crud)):
    post = add_post_to_db(post, crud=crud)
    return Msg(msg="success")


@router.get("/post-list")
def read_posts(search_info: SearchInfo, crud: CRUD = Depends(get_crud)):
    posts = get_posts_from_db(post_info=search_info)
    return [Post.from_orm(post) for post in posts]