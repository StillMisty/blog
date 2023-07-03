from fastapi import APIRouter, Cookie, File, UploadFile
from schemas.response import success, fail
from schemas.users import UserCreate, UserLogin
from schemas.articles import ArticleBase
from database.crud import *

router = APIRouter(prefix="/super", tags=["超级管理员"])

@router.post("/login", summary="超级管理员登录")
async def superuser_login(
    user : UserLogin,
):
    '''超级管理员登录'''
    if query_is_superuser(user) == False:
        return fail(msg="fail", code=404)
    else:
        return success(msg="success")

@router.post("/create", summary="超级管理员上传文章")
async def superuser_create(
    user : UserLogin,
    article : ArticleBase
):
    '''超级管理员上传文章'''
    if query_is_superuser(user) == False:
        return fail(msg="fail", code=404)
    else:
        article.category = ",".join(article.category)
        insert_article(title=article.title, content=article.content, category=article.category)
        
        return success(msg="success")
    
@router.delete("/deletearticle", summary="超级管理员删除文章")
async def superuser_delete_article(
    user : UserLogin,
    article_id : int
):
    '''超级管理员删除文章'''
    if query_is_superuser(user) == False:
        return fail(msg="fail", code=404)
    else:
        delete_article(id=article_id)
        return success(msg="success")
    
    
@router.delete("/deletecomment", summary="超级管理员删除评论")
async def superuser_delete_comment(
    user : UserLogin,
    comment_id : int
):
    '''超级管理员删除评论'''
    if query_is_superuser(user) == False:
        return fail(msg="fail", code=404)
    else:
        delete_comment(id=comment_id)
        return success(msg="success")


    
    