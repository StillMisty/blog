
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Union

from database.crud import query_user
from schemas.response import success, fail
from config import settings


router = APIRouter(prefix="/user", tags=["用户"])

HEADSHOT_DIR = settings.HEADSHOT_DIR

@router.get("/{id}" ,summary="用户详情")
async def user_detail(id: int):
    user = query_user(id=id)
    if user == []:
        return fail(code=404, msg="用户不存在")
    return success(data=user, msg="success")


@router.get("/headimg/{id}" ,summary="用户头像" ,response_class=StreamingResponse)
async def user_headimg(id: int):
    user = query_user(id=id)
    if user == []:
        return fail(code=404, msg="用户不存在")
    
    return StreamingResponse(open(HEADSHOT_DIR +'\\'+ user[0].headimg, mode="rb"), media_type="image/png")