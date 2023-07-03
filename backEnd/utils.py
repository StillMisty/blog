
import hashlib
import markdown
from http.cookies import SimpleCookie


def hash_password(password):
    '''密码加密'''
    password = password + "blog" #加盐
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashed_password = sha256_hash.hexdigest()

    return hashed_password
    

def set_cookie(emil:str, password:str):
    '''设置cookie'''
    
    cookie = SimpleCookie()
    password = hash_password(password)
    # 放弃了，不知道咋用，等后面会了再重构
    pass
    
    
def markdown_to_html(content:str):
    '''md转html'''
    content = markdown.markdown(content)
    return content