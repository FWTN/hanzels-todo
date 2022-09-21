import os
import sqlite3
import bson
from abc import ABC, abstractclassmethod
from datetime import datetime
from operator import indexOf
from uuid import UUID, uuid1
from .models import Todo
from pymongo import MongoClient


class TodoNotFoundException(Exception):
    def __init__(self, id: str) -> None:
        message = f"Todo with ID: {id} was not found"
        super().__init__(message)


def sql_from_file(filename: str) -> str:
    sql_path = os.path.dirname(os.path.realpath(__file__)) + "/sql/" + filename
    with open(sql_path) as f:
        return f.read()


def create_repository() -> "ABCTodoRepository":
    """Create repository based on value contained in PERSISTENCY enviroment variable"""
    match os.environ.get('PERSISTENCY'):
        case "memory": return InMemoryTodoRepsitory()
        case "sqlite": return SQLiteTodoRepository()
        case "mongo": return MongoTodoRepository()
        case _: raise Exception("Invalid or missing PERSISTENCY environment variable")


class ABCTodoRepository(ABC):
    @abstractclassmethod
    def connect(self) -> None: ...
    
    @abstractclassmethod
    def disconnect(self) -> None: ...
    
    @abstractclassmethod
    def find_all(self) -> list[Todo]: ...
    
    @abstractclassmethod
    def find_by_id(self, id: str) -> Todo: ...
    
    @abstractclassmethod
    def create(self, todo: Todo) -> Todo: ...
    
    @abstractclassmethod
    def delete(self, id: str) -> None: ...
    
    @abstractclassmethod
    def update(self, todo: Todo) -> Todo: ...


class InMemoryTodoRepsitory(ABCTodoRepository):
    def __init__(self) -> None:
        super().__init__()
        self.todos = [
            Todo(UUID('00000000-0000-0000-0000-000000000001'),
                 "Do your first thing", datetime.now(), 0, None),
            Todo(UUID('00000000-0000-0000-0000-000000000002'),
                 "Do 7 push ups", datetime.now(), 0, None),
            Todo(UUID('00000000-0000-0000-0000-000000000003'),
                 "Eat MC Donalds", datetime.now(), 0, None),
        ]

    def connect(self) -> None: pass
    def disconnect(self) -> None: pass

    def find_all(self) -> list[Todo]:
        return self.todos

    def find_by_id(self, id: str) -> Todo | None:
        items = [x for x in self.todos if x.id == UUID(id)]
        if items:
            return items[0]
        else:
            raise TodoNotFoundException(id) 

    def create(self, todo: Todo) -> Todo:
        self.todos.append(todo)
        return todo

    def delete(self, id: str) -> None:
        self.todos = [x for x in self.todos if x.id != UUID(id)]

    def update(self, todo: Todo) -> Todo:
        index = self.todos.index(todo)
        self.todos[index] = todo
        return todo


class SQLiteTodoRepository(ABCTodoRepository):
    def connect(self) -> None:
        self.connection = sqlite3.connect("todo.sqlite")
        sql = sql_from_file("init.sql")
        cursor = self.connection.cursor()
        cursor.executescript(sql)
        self.connection.commit()

    def disconnect(self) -> None:
        self.connection.close()

    def find_all(self) -> list[Todo]:
        cursor = self.connection.cursor()
        result = cursor.execute("select * from todos")
        todos = [Todo(*x) for x in result.fetchall()]
        return todos

    def find_by_id(self, id: str) -> Todo:
        cursor = self.connection.cursor()
        result = cursor.execute(f"select * from todos where id = '{id}'")
        todo = result.fetchone()
        return Todo(*todo)

    def create(self, todo: Todo) -> Todo:
        cursor = self.connection.cursor()
        sql = f"insert into todos values (?, ?, ?, ?, ?)"
        cursor.execute(sql, (str(todo.id), todo.text, todo.status,
                       todo.create_time, todo.resolve_time))
        self.connection.commit()
        return todo

    def update(self, todo: Todo) -> Todo:
        cursor = self.connection.cursor()
        sql = f"update todos set content = ?, stat = ?, resolve_time = ? where id = ?"
        cursor.execute(sql, (todo.text, todo.status,
                       todo.resolve_time, (str(todo.id))))
        self.connection.commit()
        return todo

    def delete(self, id: str) -> None:
        cursor = self.connection.cursor()
        result = cursor.execute(f"delete from todos where id = '{id}'")
        self.connection.commit()


class MongoTodoRepository(ABCTodoRepository):
    def connect(self) -> None:
        self.client = MongoClient(
            host=os.environ.get("MONGO_HOST"),
            port=int(os.environ.get("MONGO_PORT")),
            username=os.environ.get("MONGO_USER"),
            password=os.environ.get("MONGO_PASS")
        )
        self.client.rptodos.todos.drop()

        # initialize database
        todo1 = Todo(UUID('00000000-0000-0000-0000-000000000001'),
                     "Do your first thing", datetime.now(), 0, None)
        todo2 = Todo(UUID('00000000-0000-0000-0000-000000000002'),
                     "Do 7 push ups", datetime.now(), 0, None)
        todo3 = Todo(UUID('00000000-0000-0000-0000-000000000003'),
                     "Eat MC Donalds", datetime.now(), 0, None)
        self.create(todo1)
        self.create(todo2)
        self.create(todo3)

    def disconnect(self) -> None:
        self.client.close()

    def find_all(self) -> list[Todo]:
        db = self.client.rptodos
        todos = [Todo(x.get("_id").as_uuid(), x.get('text'), x.get('status'), x.get(
            'create_time'), x.get('validate_time')) for x in db.todos.find()]
        return todos

    def find_by_id(self, id: str):
        raise Exception("Not implemented")

    def create(self, todo: Todo) -> Todo:
        db = self.client.rptodos
        todos = db.todos
        todos.insert_one({
            "_id": bson.Binary.from_uuid(todo.id),
            "text": todo.text,
            "status": todo.status,
            "create_time": todo.create_time,
            "resolve_time": todo.resolve_time
        })

    def update(self, todo: Todo) -> Todo:
        raise Exception("Not implemented")

    def delete(self, id: str) -> None:
        raise Exception("Not implemented")
