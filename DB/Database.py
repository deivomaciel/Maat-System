from tortoise import Tortoise

class Database:
    def __init__(self):
        self.__connection = None

    async def connect(self, url_connection: str):
        self.__connection = await Tortoise.init(
            db_url=url_connection, 
            modules={'models': ['Model.UserModel', 'Model.LinkModel']},
        )

        await Tortoise.generate_schemas()

