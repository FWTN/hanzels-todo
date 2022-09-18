from datetime import datetime
from uuid import UUID, uuid1
from todo import app, repository
from todo.models import Todo
from quart import request, render_template


@app.get('/')
async def index():
    return await render_template("index.html")


@app.get('/todo')
async def todo_list():
    data = repository.find_all()
    return {"message": "succes", "data": data}


@app.get('/todo/<id>')
async def todo_by_id(id: str):
    try:
        data = repository.find_by_id(id)
        return {"message": "succes", "data": data}

    except Exception as ex:
        return {"message": "failure", "error": str(ex)}


@app.post('/todo')
async def new_toto():
    data = await request.json
    try:
        todo = repository.create(
            Todo(id=uuid1(),
                 text=data["text"],
                 create_time=datetime.now(),
                 status=0,
                 resolve_time=None)
        )
        return {"message": "success", "data": todo}

    except Exception as ex:
        return {"message": "failure", "error": str(ex)}


@app.put('/todo')
async def update():
    data = await request.json
    try:
        todo = repository.update(
            Todo(id=UUID(data["id"]),
                 text=data["text"],
                 create_time=data["create_time"],
                 status=data["status"],
                 resolve_time=data["resolve_time"]
                 ))
        return {"message": "success", "data": todo}

    except Exception as ex:
        return {"message": "failure", "error": str(ex)}


@app.delete('/todo/<id>')
async def delete(id: str):
    try:
        repository.delete(id)
        return {"message": "delete succes"}
    except Exception as ex:

        return {"message": "failure", "error": str(ex)}
