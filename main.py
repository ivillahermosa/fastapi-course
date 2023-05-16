from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


my_posts = [{"title": "title of post 1",
             "content": "content of post 1", "id": 1},
            {"title": "title of post 2",
             "content": "content of post 2", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/posts")
def get_posts():
    return {"data": "This is your post!!!"}


# add status code in parameter for return
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    return {"message": "successfully created postss!!"}


# use HttpException from now on
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}
