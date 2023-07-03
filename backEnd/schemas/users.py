
from pydantic import BaseModel, EmailStr, FileUrl

class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str
    headimg: FileUrl
