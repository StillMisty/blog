from datetime import datetime
from typing import List
from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str
    
class ArticleCreate(ArticleBase):
    id: int
    category: List[str]

class Article(ArticleCreate):
    views: int

