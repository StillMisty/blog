
from fastapi import APIRouter

from typing import Union

from database.crud import query_article_list, query_article_count, query_article,query_article_category,query_article_comment,query_user
from schemas.response import success, fail
from config import settings
import utils


router = APIRouter(prefix="/article", tags=["文章"])

ARTICLE_PRE_PAGE = settings.ARTICLES_PER_PAGE
HEADSHOT_DIR = settings.HEADSHOT_DIR


@router.get("/list/{page}" ,summary="文章列表")
async def article_list(page: Union[int, None] = None):
    if page is None or page < 1:
        page = 1
        
    article_count = query_article_count()
    if page > article_count//ARTICLE_PRE_PAGE + 1:
        return fail(code=404, msg="没有更多文章了")
    
    article_list = query_article_list(page=page, limit=ARTICLE_PRE_PAGE)

    
    for article in article_list:
        article.create_time = article.create_time.strftime(r"%Y-%m-%d %H:%M:%S")
        article.category = article.category.split(",")
    
    return success(data={"all_articles": article_list, "total": article_count}, msg="success")


@router.get("/detail/{id}" ,summary="文章详情")
async def article_detail(id: int):
    if utils.article_filer(id=id) is False:
        return fail(code=404, msg="文章不存在")
    
    article = query_article(id=id)
    article.create_time = article.create_time.strftime(r"%Y-%m-%d %H:%M:%S")
    article.category = article.category.split(",")
    
    return success(data=article, msg="success")
    
    
@router.get("/category/{category}" ,summary="分类中的所有文章")
async def article_category(category: str):
    category_list = query_article_category(category=category)
    
    if category_list is None:
        return fail(code=404, msg="分类不存在")
    
    return success(data=category_list, msg="success")


@router.get("/comment/{id}" ,summary="文章评论")
async def article_comment(id: int):
    if utils.article_filer(id=id) is False:
        return fail(code=404, msg="文章不存在")
    
    comments = query_article_comment(id=id)
    for comment in comments:
        user = query_user(id=comment.user_id)
        comment.user_id = user
    
    return success(data=comments, msg="success")


    
    
    
    
    
    

