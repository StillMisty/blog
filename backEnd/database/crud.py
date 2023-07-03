
from config import settings
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy import  Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker, Session
from  sqlalchemy import create_engine
from datetime import datetime
from typing import List


class BaseService(object):
    engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
    Session = sessionmaker(bind = engine)
    session = Session()

Base=declarative_base()
class users(Base):
    # 表名
    __tablename__='users'
    # 字段，属性
    id=Column(Integer,primary_key=True, autoincrement=True) #自增
    username=Column(String(50))
    email=Column(String(50), unique=True)
    head_img=Column(String(50))
    
class articles(Base):
    __tablename__='articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    content = Column(String(50))
    create_time = Column(DateTime)
    category = Column(String(50))
    views = Column(Integer)
    
class comments(Base):
    __tablename__='comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(200))
    create_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))
    
#建表
def create_table():
    Base.metadata.create_all(BaseService.engine)
    
#插入
def insert_article(
    title: str, 
    content :str, 
    create_time :datetime,
    category : List[str],
    views :int
):
    article = articles(title=title,content=content,create_time=create_time,category=category,views=views)
    BaseService.session.add(article)
    BaseService.session.commit()
    
#查询
def query_article(
    id: int
) -> articles:
    '''返回文章详情'''
    article=BaseService.session.query(articles).filter(articles.id==id).all()
    return article

def query_article_list(
    page: int,
    limit: int
) -> List[articles]:
    '''返回文章列表'''
    article=BaseService.session.query(articles).order_by(articles.id.desc()).limit(limit).offset((page-1)*limit).all()
    return article

def query_article_count() -> int:
    """返回总文章数"""
    article_count = BaseService.session.query(articles).count()
    return article_count

def query_user(
    id: int
) -> users:
    '''返回用户详情'''
    user=BaseService.session.query(users).filter(users.id==id).all()
    return user

def query_comment(
    id: int
) -> comments:
    '''返回评论详情'''
    comment=BaseService.session.query(comments).filter(comments.id==id).all()
    return comment

def query_article_comment(
    article_id: int
) -> List[comments]:
    '''返回文章评论'''
    comment=BaseService.session.query(comments).filter(comments.article_id==article_id).all()
    return comment

def query_article_category(
    category: str
) -> List[articles]:
    '''返回所属分类的文章'''
    article=BaseService.session.query(articles).filter(articles.category in category).all()
    return article