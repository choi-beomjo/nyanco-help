from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
#from db.crud.crud import get_crud, CRUD
from .utils import *
from .schemas import *
from ...deps import get_current_user, get_crud, CRUD

router = APIRouter(tags=[Tags.board])


@router.get("/board")
def get_test_code(crud: CRUD = Depends(get_crud)):
    return Msg(msg="success")


@router.get("/post-all")
def read_all_posts(crud: CRUD = Depends(get_crud)):
    posts = get_posts_from_db(crud=crud)
    return [PostInfo.from_orm(post) for post in posts]


@router.post("/post")
def add_post(post: Post,crud: CRUD = Depends(get_crud), current_user = Depends(get_current_user)):
    db_post = add_post_to_db(post_info=post, user=current_user, crud=crud)
    return Msg(msg="success")


@router.post("/post-list")
def read_posts(search_info: SearchInfo, crud: CRUD = Depends(get_crud), current_user = Depends(get_current_user)):
    posts = get_posts_from_db(post_info=search_info, crud=crud)
    return [Post.from_orm(post) for post in posts]


@router.get('/user-post')
def get_posts_by_user(crud: CRUD = Depends(get_crud), current_user = Depends(get_current_user)):
    posts = get_posts_from_db(user=current_user, crud=crud)
    return [Post.from_orm(post) for post in posts]


@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, crud: CRUD = Depends(get_crud)):
    post = get_post_from_db(post_id=post_id, crud=crud)
    return Post.from_orm(post)

