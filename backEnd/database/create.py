import sqlite3

from config import settings
from pathlib import Path
#SQLAlchemy不允许修改表结构，所以这里使用sqlite3

def init_db():
    '''
    初始化数据库
    '''
    database_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
    
    if not database_path.exists():
        conn = sqlite3.connect(database_path)
        
        #建表
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mail TEXT NOT NULL UNIQUE,  
            headshot TEXT DEFAULT 'default.png',
            COMMENT 'User table'
        );''')
        #创建文章表
        cursor.execute("""
        CREATE TABLE articles (
           id INTEGER PRIMARY KEY AUTOINCREMENT, 
           title VARCHAR(100) NOT NULL,
           content TEXT NOT NULL,    
           create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
           COMMENT 'Article table'
        );""")
        #创建评论表
        cursor.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            article_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,      
            content TEXT NOT NULL,
            create_time DATETIME NOT NULL,
            FOREIGN KEY (article_id) REFERENCES articles(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );''')
        
        conn.commit()
        conn.close()

    



