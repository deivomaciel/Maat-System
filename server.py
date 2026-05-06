from fastapi import FastAPI
from os import getenv
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise

from Controller.UserController import user_router

load_dotenv()
app = FastAPI()

register_tortoise(
    app,
    db_url=getenv('DATABASE_URL'),
    modules={'models': ['Model.UserModel', 'Model.LinkModel', 'Model.RatingModel']},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "API rodando 🚀"}