from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def super():
    '''
    管理员页面
    '''
    
    file = open("./static/index.html", encoding="utf-8").read()
    
    return HTMLResponse(content=file, status_code=200)