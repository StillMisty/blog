
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import copy
import os
from database.crud import query_user,insert_user,query_user_email
from schemas.response import success, fail
from schemas.users import UserCreate, UserDetail
from config import settings


router = APIRouter(prefix="/user", tags=["用户"])

HEADSHOT_DIR = settings.HEADSHOT_DIR

@router.get("/{id}" ,summary="用户详情")
async def user_detail(id: int):
    user = query_user(id=id)
    if user == None:
        return fail(code=404, msg="用户不存在")
    user = copy.deepcopy(user)
    user = UserDetail(**user.__dict__)
    return success(data=user, msg="success")


@router.get("/headimg/{id}" ,summary="用户头像" ,response_class=StreamingResponse)
async def user_headimg(id: int):
    user = query_user(id=id)
    if user == None:
        return fail(code=404, msg="用户不存在")
    
    return StreamingResponse(open(os.path.join(HEADSHOT_DIR, user.headimg), mode="rb"), media_type="image/png")

@router.post("create" ,summary="创建用户")
async def user_create(
    user: UserCreate
):
    if query_user_email(email=user.email) != None:
        return fail(code=400, msg="邮箱已存在")
    
    insert_user(email=user.email,password=user.password,username=user.username)
    return success(msg="success")