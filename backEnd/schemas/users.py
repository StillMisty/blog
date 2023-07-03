
from pydantic import BaseModel, EmailStr, FileUrl

class UserBase(BaseModel):
    email: EmailStr
    username: str
    headimg: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(UserBase):
    password: str
    
class UserDetail(UserBase):
    id: int
    is_superuser: bool
    
