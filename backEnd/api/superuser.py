from fastapi import APIRouter, Cookie, File, UploadFile
from schemas.response import success, fail
from schemas.users import UserCreate
from schemas.articles import ArticleCreate
from database.crud import *

router = APIRouter(prefix="/super", tags=["超级管理员"])

@router.get("/login")
async def superuser_login(
    user : UserCreate,
):
    '''超级管理员登录'''
    if query_is_superuser(user) == False:
        return fail("登录失败")
    else:
        return success("登录成功")

@router.post("/create")
async def superuser_create(
    user : UserCreate,
    article : ArticleCreate
):
    '''超级管理员上传文章'''
    if query_is_superuser(user) == False:
        return fail("上传失败")
    else:
        
        insert_article(title=article.title, content=article.content, category=article.category)
        
        return success("上传成功")
    
@router.post("/deletearticle")
async def superuser_delete_article(
    user : UserCreate,
    article_id : int
):
    '''超级管理员删除文章'''
    if query_is_superuser(user) == False:
        return fail("删除失败")
    else:
        delete_article(id=article_id)
        return success("删除成功")
    
@router.post("/deletecomment")
async def superuser_delete_comment(
    user : UserCreate,
    comment_id : int
):
    '''超级管理员删除评论'''
    if query_is_superuser(user) == False:
        return fail("删除失败")
    else:
        delete_comment(id=comment_id)
        return success("删除成功")


    
    