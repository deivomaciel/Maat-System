from DB.Database import Database
from Repository.UserRepository import UserRepository
import asyncio

database = Database()

async def start():
    await database.connect('postgres://neondb_owner:npg_EvI0cnqe5uGw@ep-dry-water-an4grr0p-pooler.c-6.us-east-1.aws.neon.tech/MeetS')
    user = await UserRepository().createUser('teste', 'addadsadasda', '12345678')
    print(user)

asyncio.run(start())