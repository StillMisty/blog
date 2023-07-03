
from pydantic import BaseModel, EmailStr, FileUrl

class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str
    head_img: FileUrl
