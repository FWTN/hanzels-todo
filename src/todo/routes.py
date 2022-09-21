from todo import app, repository
from todo.models import Todo
from quart import request, render_template, jsonify
from functools import wraps


def error_catcher(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return jsonify(
                await func(*args, **kwargs)
            )
        except Exception as ex:
            return {"error": str(ex)}
    return wrapper


@app.get('/')
async def index():
    return await render_template("index.html")


@app.get('/todo')
@error_catcher
async def todo_list():
    return repository.find_all()


@app.get('/todo/<id>')
@error_catcher
async def todo_by_id(id: str):
    return repository.find_by_id(id)


@app.post('/todo')
@error_catcher
async def new_toto():
    data = await request.json
    todo = repository.create(Todo.from_text(data["text"]))
    return todo


@app.put('/todo')
@error_catcher
async def update():
    json = await request.json
    todo = repository.update(Todo.from_json(json))
    return todo


@app.delete('/todo/<id>')
@error_catcher
async def delete(id: str):
    repository.delete(id)
    return {"message": "delete succes"}
