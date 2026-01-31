import os
from datetime import datetime
from typing import List

import httpx
import uvicorn
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field, constr

AUTH_API_URL = os.getenv("AUTH_API_URL", "http://authapi:9000")

app = FastAPI()


class NewPost(BaseModel):
    korisnik: constr(max_length=20)
    tekst: constr(max_length=280)
    vrijeme: datetime


class Post(NewPost):
    id: int


class Credentials(BaseModel):
    korisnicko_ime: constr(max_length=20)
    lozinka: str


objave: List[Post] = []
_next_id = 1


def _next_post_id() -> int:
    global _next_id
    value = _next_id
    _next_id += 1
    return value


@app.post("/objava", response_model=Post)
async def create_post(payload: NewPost) -> Post:
    post = Post(id=_next_post_id(), **payload.model_dump())
    objave.append(post)
    return post


@app.get("/objava/{id}", response_model=Post)
async def get_post(id: int) -> Post:
    for post in objave:
        if post.id == id:
            return post
    raise HTTPException(status_code=404, detail="Post not found.")


@app.get("/korisnici/{korisnik}/objave", response_model=List[Post])
async def get_user_posts(
    korisnik: str,
    credentials: Credentials = Body(...),
) -> list[Post]:
    if korisnik != credentials.korisnicko_ime:
        raise HTTPException(status_code=400, detail="Username is not valid.")

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{AUTH_API_URL}/login", json=credentials.model_dump()
            )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="AuthAPI is down.")

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid login data.")

    data = response.json()
    if not data.get("authorized"):
        raise HTTPException(status_code=401, detail="Invalid login data.")

    return [post for post in objave if post.korisnik == korisnik]


# # how to dockerize
# docker build -t socialapi .
# docker run --rm -p 3500:3500 socialapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3500)
