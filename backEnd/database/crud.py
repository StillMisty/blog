
from config import settings
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy import  Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker
from  sqlalchemy import create_engine
from datetime import datetime
from typing import List
import copy
import os

from utils import hash_password, markdown_to_html
from schemas.users import UserLogin
from config import settings

ARTICLE_DIR = settings.ARTICLE_DIR

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
    headimg=Column(String(50), default='default.png')
    password=Column(String(50))
    is_superuser=Column(Integer, default=0)
    cookie=Column(String(50))
    
class articles(Base):
    __tablename__='articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    content = Column(String(200))
    create_time = Column(DateTime, default=datetime.now())
    category = Column(String(50))
    views = Column(Integer, default=0)
    is_delete = Column(Integer, default=0)
    
class comments(Base):
    __tablename__='comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(200))
    create_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))
    is_delete = Column(Integer, default=0)
    
#建表
def create_table():
    Base.metadata.create_all(BaseService.engine)
    
#插入
def insert_article(
    title: str, 
    content :str, 
    category : List[str],
):
    id = BaseService.session.query(articles.id.desc()).scalar()
    with open(os.path.join(ARTICLE_DIR,str(id) + '.md'), "w") as f:
        f.write(content)
    content = content[:200] if len(content) > 200 else content
    article = articles(title=title,content=content,category=category)
    BaseService.session.add(article)
    BaseService.session.commit()

def insert_user(
    email: str,
    username: str,
    password: str
):
    password = hash_password(password) #密码加密
    user = users(email=email,password=password,username=username)
    BaseService.session.add(user)
    BaseService.session.commit()
    
def insert_comment(
    content: str,
    user_id: int,
    article_id: int
):
    content = content[:200] if len(content) > 200 else content
    comment = comments(content=content,user_id=user_id,article_id=article_id)
    BaseService.session.add(comment)
    BaseService.session.commit()

#查询
def query_article(
    id: int
) -> articles:
    '''返回文章详情'''
    article=BaseService.session.query(articles).filter(articles.id==id).first()
    article = copy.deepcopy(article)
    article.content = open(os.path.join(ARTICLE_DIR, str(article.id) + '.md'), mode="r", encoding="utf-8").read()
    article.content = markdown_to_html(article.content)
    return article

def query_article_list(
    page: int,
    limit: int
) -> List[articles]:
    '''返回文章列表'''
    article=BaseService.session.query(articles).order_by(articles.id.desc()).filter(articles.is_delete == 0).limit(limit).offset((page-1)*limit).all()
    return article

def query_article_count() -> int:
    """返回总文章数"""
    article_count = BaseService.session.query(articles.id.desc()).first()[0]
    return article_count

def query_user(
    id: int
) -> users:
    '''返回用户详情'''
    user=BaseService.session.query(users).filter(users.id==id).first()
    return user

def query_comment(
    id: int
) -> comments:
    '''返回评论详情'''
    comment=BaseService.session.query(comments).filter(comments.id==id).first()
    return comment

def query_article_comment(
    id: int
) -> List[comments]:
    '''返回文章评论'''
    comment=BaseService.session.query(comments).filter(comments.article_id==id and comments.is_delete==0).all()
    return comment

def query_article_category(
    category: str
) -> List[articles]:
    '''返回所属分类的文章'''
    article=BaseService.session.query(articles).filter(articles.is_delete == 0).all()
    article_list = [i for i in article if category in i.category]
    return article_list
    
def query_user_email(
    email: str
) -> users | None:
    '''返回邮箱所属用户'''
    user = BaseService.session.query(users).filter(users.email==email).first()
    return user

def query_user_password(
    email: str,
    password: str
) -> bool:
    '''返回用户密码是否正确'''
    user = BaseService.session.query(users).filter(users.email==email).first()
    if user == None:
        return False
    
    password = hash_password(password)
    if password == user.password:
        return True
    else:
        return False
    
def query_is_superuser(
    user: UserLogin
):
    '''返回用户是否是超级管理员'''
    user_email = query_user_email(user.email)
    if user_email == None:
        return False
    user_password = query_user_password(user.email, user.password)
    if user_password == False:
        return False
    user = BaseService.session.query(users).filter(users.email==user.email and users.is_superuser == 1).first()
    if user == None:
        return False
    else:
        return True
    
#更新
def update_article_views(
    id: int,
):
    '''更新文章浏览量'''
    article = BaseService.session.query(articles).filter(articles.id==id).first()
    article.views += 1
    BaseService.session.commit()
    
#删除
def delete_article(
    id: int
):
    '''删除文章'''
    article = BaseService.session.query(articles).filter(articles.id==id).first()
    article.is_delete = 1
    BaseService.session.commit()

def delete_comment(
    id: int
):
    '''删除评论'''
    comment = BaseService.session.query(comments).filter(comments.id==id).first()
    comment.is_delete = 1
    BaseService.session.commit()