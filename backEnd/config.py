import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings
from typing import List


class Config(BaseSettings):
    # 加载环境变量
    load_dotenv(find_dotenv(), override=True)
    # 调试模式
    APP_DEBUG: bool = True
    # 静态资源目录
    STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    TEMPLATE_DIR: str = os.path.join(STATIC_DIR, "templates")
    ARTICLE_DIR: str = os.path.join(STATIC_DIR, "articles")
    HEADSHOT_DIR: str = os.path.join(STATIC_DIR, "headshots")
    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./blog.db"
    DATABASE_ECHO: bool = True
    #每页的文章数量
    ARTICLES_PER_PAGE: int = 10
    

settings = Config()