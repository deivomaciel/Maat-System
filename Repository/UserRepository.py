from Model.UserModel import User
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class UserRepository():
    
    async def createUser(self, name: str, email: str, password: str):
        user = User(name=name, email=email, password=password_hash.hash(password))
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
                    setattr(user, 'password', password_hash.hash(new_value))

                case _:
                    return None
                

            await user.save()
        return user
    

    async def userLogin(self, email: str, password: str):
        user = await User.get_or_none(email=email)

        if user:
            if password_hash.verify(password, user.password):
                return {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                }

            else: return None