from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from os import getenv, path
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.sessions import SessionMiddleware

from Controller.UserController import user_router
from Controller.LinkController import link_router
from Controller.ViewController import view_router

load_dotenv()

BASE_DIR = path.dirname(path.abspath(__file__))

app = FastAPI(title="Maat")

app.add_middleware(SessionMiddleware, secret_key=getenv("SECRET_KEY", "maat-dev-secret-2024"))
app.mount("/static", StaticFiles(directory=path.join(BASE_DIR, "static")), name="static")

register_tortoise(
    app,
    db_url=getenv('DATABASE_URL'),
    modules={'models': ['Model.UserModel', 'Model.LinkModel', 'Model.RatingModel']},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(user_router)
app.include_router(link_router)
app.include_router(view_router)
