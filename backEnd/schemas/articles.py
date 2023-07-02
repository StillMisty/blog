from datetime import datetime
from typing import List
from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str
    
class ArticleCreate(ArticleBase):
    id: int
    create_time: datetime
    category: List[str]
    views: int

