
from fastapi import APIRouter, Cookie, Query

from typing import Union

from database.crud import *
from schemas.response import success, fail
from schemas.users import UserCreate
from config import settings

import copy

router = APIRouter(prefix="/article", tags=["文章"])

ARTICLE_PRE_PAGE = settings.ARTICLES_PER_PAGE
HEADSHOT_DIR = settings.HEADSHOT_DIR


@router.get("/list/{page}" ,summary="文章列表")
async def article_list(page: Union[int, None] = 1):
    if page is None or page < 1:
        page = 1
        
    article_count = query_article_count()
    if page > article_count//ARTICLE_PRE_PAGE + 1:
        return fail(code=404, msg="没有更多文章了")
    
    article_list = copy.deepcopy(query_article_list(page=page, limit=ARTICLE_PRE_PAGE))

    
    for article in article_list:
        article.create_time = article.create_time.strftime(r"%Y-%m-%d %H:%M:%S")
        article.category = article.category.split(",")
    
    return success(data={"all_articles": article_list, "total": article_count}, msg="success")


@router.get("/detail/{id}" ,summary="文章详情")
async def article_detail(id: int):
    if (id is None) or (id < 1) or (id > query_article_count()):
        return fail(code=404, msg="文章不存在")
    
    update_article_views(id=id)
    
    article = copy.deepcopy(query_article(id=id))
    article.create_time = article.create_time.strftime(r"%Y-%m-%d %H:%M:%S")
    article.category = article.category.split(",")
    
    return success(data=article, msg="success")
    
    
@router.get("/category/{category}" ,summary="分类中的所有文章")
async def article_category(category: str):
    category_list = query_article_category(category=category)
    
    if category_list == []:
        return fail(code=404, msg="分类不存在")
    
    return success(data=category_list, msg="success")


@router.get("/comment/{id}" ,summary="文章评论")
async def article_comment(id: int):
    if (id is None) or (id < 1) or (id > query_article_count()):
        return fail(code=404, msg="文章不存在")
    
    comments = query_article_comment(id=id)
    for comment in comments:
        user = query_user(id=comment.user_id)
        comment.user_id = user
    
    return success(data=comments, msg="success")


@router.post("/comment/{id}" ,summary="评论文章")
async def post_comment(
    id: int,
    user: UserCreate,
    comment: str = Query(..., min_length=1, max_length=200)
):
    if not query_user_password(email=user.email,password=user.password):
        return fail(code=400, msg="邮箱或密码错误")
    
    if (id is None) or (id < 1) or (id > query_article_count()):
        return fail(code=404, msg="文章不存在")
    
    user_id = query_user_email(email=user.email).id
    
    insert_comment(content=comment,user_id=user_id,article_id=id)
    
    return success(msg="success")
