from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):  # inherit the created models no need to specify
    id: int
    # created_at: datetime

    # converting sql alchemy model to pydantic model
    class Config:
        orm_mode = True
