from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# python -m uvicorn hmw_5:app

app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
def new_req(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}')
def get_user(request: Request, user_id: int):
    for user in users:
        if user_id == user.id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})


@app.post('/user/{username}/{age}')
def create_user(username: str, age: int, user: User):
    user.username = username
    user.age = age
    if len(users) == 0:
        user.id = 1
    else:
        last = users[-1]
        user.id = last.id + 1
    users.append(user)
    return f'Пользователь создан. Ваш уникальный айди: <{user.id}>'


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user_id == user.id:
            user.username = username
            user.age = age
            return f'Пользователь с айди {user_id} обновлён'
    else:
        raise HTTPException(status_code=404, detail='Пользователь не найден')


@app.delete('/user/{user_id}')
def delete_user(user_id: int):
    for user in users:
        if user_id == user.id:
            users.remove(user)
            return f'Пользователь с айди {user_id} удалён'
    else:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
