from datetime import datetime
from typing import List
from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str
    category: List[str]

class Article(ArticleBase):
    views: int

