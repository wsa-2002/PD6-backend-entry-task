from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from datetime import datetime
from databases import Database
from dataclasses import dataclass
from typing import Sequence
from config import db_config
from config import app_config

app = FastAPI(
    title=app_config.title,
    docs_url=app_config.docs_url,
    redoc_url=app_config.redoc_url,
)

database = Database(db_config.host, port=db_config.port, user=db_config.username, password=db_config.password,
                    database=db_config.db_name)


@dataclass
class PostOutput:
    id: int
    name: str
    content: str
    time: datetime


@dataclass
class CommentOutput:
    id: int
    post_id: int
    name: str
    message: str
    time: datetime


@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def default_page():
    doc_path = "<a href=\"/docs\">/docs</a>"
    return doc_path


@app.get("/post", tags=['Post'])
async def browse_post() -> Sequence[PostOutput]:
    query = "SELECT id, name, content, time  " \
            "       FROM post " \
            "   ORDER BY id ASC"
    result = await database.fetch_all(query=query)
    return [PostOutput(id=int(result[i]["id"]),
                       name=result[i]["name"],
                       content=result[i]["content"],
                       time=result[i]["time"])
            for i in range(len(result))]


@app.post("/post", tags=['Post'])
async def add_post(name: str, content: str) -> int:
    query = "INSERT INTO post(name, content, time) " \
            "       VALUES ('{}','{}','{}')" \
            "   RETURNING id ".format(name, content, datetime.now())
    result = await database.fetch_one(query=query)
    result = int(result["id"])
    return result


@app.get("/post/{id}", tags=['Post'])
async def read_post(post_id: int) -> PostOutput:
    query = "SELECT id, name, content, time" \
            "       FROM post" \
            "   WHERE id = {}".format(post_id)
    result = await database.fetch_all(query=query)
    if not result:
        raise HTTPException(status_code=404, detail="post_id not found")
    return PostOutput(id=int(result[0]["id"]),
                      name=result[0]["name"],
                      content=result[0]["content"],
                      time=result[0]["time"])


@app.delete("/post/{id}", tags=['Post'])
async def delete_post(post_id: int) -> str:
    query = "DELETE FROM post" \
            "   WHERE id = {}".format(post_id)
    await database.fetch_all(query=query)
    return f"post {post_id} is deleted."


@app.patch("/post/{id}", tags=['Post'])
async def edit_post(post_id: int, name: str = None, content: str = None) -> str:
    set_sql = fr""
    if name is not None:
        set_sql = set_sql + fr"name='{name}'"

    if content is not None:
        if name is not None:
            set_sql = set_sql + ", "
        set_sql = set_sql + fr"content='{content}'"
    query = "UPDATE post" \
            "       SET {}" \
            "   WHERE id = {}".format(set_sql, post_id)
    await database.fetch_one(query=query)
    return f"post {post_id} has been edited."


@app.get("/post/{post_id}/comment", tags=['Comment'])
async def browse_comments(post_id: int) -> Sequence[CommentOutput]:
    query = "SELECT id, name, message, time" \
            "       FROM comment" \
            "   WHERE post_id = {};".format(post_id)
    result = await database.fetch_all(query=query)
    if not result:
        raise HTTPException(status_code=404, detail="post_id not found")
    return [CommentOutput(id=int(result[i]["id"]),
                          post_id=post_id,
                          message=result[i]["message"],
                          name=result[i]["name"],
                          time=result[i]["time"])
            for i in range(len(result))]


@app.post("/post/{post_id}/comment", tags=['Comment'])
async def add_comment(post_id: int, name: str, message: str) -> int:
    query = "INSERT INTO comment(post_id, name, message, time)" \
            "       VALUES ('{}','{}','{}','{}')" \
            "   RETURNING id ".format(post_id, name, message, datetime.now())
    result = await database.fetch_all(query=query)
    return int(result[0]["id"])
