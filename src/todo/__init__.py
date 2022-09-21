import atexit
from quart import Quart
from .repositories import create_repository
from dotenv import load_dotenv

load_dotenv()

app = Quart(__name__)

try:
    repository = create_repository()
    repository.connect()
except Exception as ex:
    print("Error during repository initialization")
    print(str(ex))


def run() -> None:
    app.run()


atexit.register(repository.disconnect)


if __name__ == "__main__":
    run()


from .routes import *
