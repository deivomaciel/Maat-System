from Model.UserModel import User

class UserRepository():
    
    async def createUser(self, name: str, email: str, password: str):
        user = User(name=name, email=email, password=password)
        await user.save()
        return user

    async def deleteUser(self, id: int):
        user = await User.get_or_none(id=id)

        if user:
            await user.delete()

        return user
    
    async def updateUserInfo(self, fields: list, new_value: str, id: int):
        user = await User.get_or_none(id=id)

        if user:
            for field in fields:
                setattr(user, field, new_value)

            await user.save()

        return user