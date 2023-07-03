
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index():
    '''
    首页
    '''
    
    file = open("./static/index.html", encoding="utf-8").read()
    
    return HTMLResponse(content=file, status_code=200)


    