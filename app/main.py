from fastapi import Body, FastAPI, HTTPException, status, Depends, Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .routers import post, user, auth

# this will create the tables in postgress
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', port=54321,
                                user='postgres', password='sa', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed!!!")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1",
             "content": "content of post 1", "id": 1},
            {"title": "title of post 2",
             "content": "content of post 2", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


# call router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
