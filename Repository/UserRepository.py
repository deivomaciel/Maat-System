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
    
    async def updateUserInfo(self, field: str, new_value: str, id: int):
        user = await User.get_or_none(id=id)

        if user:
            match field:
                case 'name':
                    setattr(user, 'name', new_value)

                case 'password':
                    setattr(user, 'password', new_value)

                case _:
                    return None
                

            await user.save()

        return user