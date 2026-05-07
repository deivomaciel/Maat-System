from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path
from os import getenv
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise

from Controller.UserController import user_router
from Controller.LinkController import link_router

load_dotenv()
app = FastAPI()

BASE_DIR = Path(__file__).parent

views = Jinja2Templates(directory=str(BASE_DIR / 'View'))

app.mount('/Static', StaticFiles(directory=str(BASE_DIR / 'Static')), name='static')

register_tortoise(
    app,
    db_url=getenv('DATABASE_URL'),
    modules={'models': ['Model.UserModel', 'Model.LinkModel', 'Model.RatingModel']},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(user_router)
app.include_router(link_router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return views.TemplateResponse(
        request=request,
        name='HomeView.html',
    )

@app.get("/login", response_class=HTMLResponse)
async def home(request: Request):
    return views.TemplateResponse(
        request=request,
        name='LoginView.html',
    )

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return views.TemplateResponse(
        request=request,
        name='RegisterView.html',
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return views.TemplateResponse(
        request=request,
        name='DashboardView.html',
    )