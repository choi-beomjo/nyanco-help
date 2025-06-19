from fastapi import HTTPException
from .models import Post
from db.crud.crud import CRUD


def get_post_from_db(post_id: int, crud: CRUD):
    db_post = crud.get(Post, obj_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail=f"Post not found: {post_id}")
    return db_post


def get_posts_from_db(crud: CRUD, post_info={}, user=None):
    filters = {key: value for key, value in post_info if value}
    if user:
        filters.update(dict(user=user))
    db_posts = crud.list(Post, filters=filters)
    return db_posts


def add_post_to_db(post_info: Post, user, crud: CRUD):
    return crud.create(Post(**post_info.dict(), user=user))


def delete_post_from_db(post_id: int, crud: CRUD):
    db_post = crud.delete(Post, obj_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail=f"Post not found: {post_id}")