import os
from quart import Quart
from .repositories import create_repository
from dotenv import load_dotenv

load_dotenv() 

app = Quart(__name__)

repository = create_repository()

def run() -> None:
    repository.connect()
    app.run()
    repository.disconnect()

from .routes import *