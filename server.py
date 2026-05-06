from DB.Database import Database

from Repository.UserRepository import UserRepository
from Repository.LinkRepository import LinkRepository

import asyncio
from os import getenv
from dotenv import load_dotenv

load_dotenv()

database = Database()

async def start():
    await database.connect(getenv('DATABASE_URL'))

asyncio.run(start())