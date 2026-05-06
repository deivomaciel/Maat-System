from tortoise import Tortoise

class Database:

    async def connect(self, url_connection: str):
        await Tortoise.init(
            db_url=url_connection, 
            modules={'models': ['Model.UserModel', 'Model.LinkModel', 'Model.RatingModel']},
        )

        await Tortoise.generate_schemas()

