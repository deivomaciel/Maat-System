from fastapi import APIRouter, status, HTTPException
from Repository.UserRepository import UserRepository
from Schemas.UserSchema import UserCreate, UserUpdate, UserDelete
from tortoise.exceptions import IntegrityError

user_router = APIRouter(prefix='/user', tags=['User'])

@user_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    try:
        new_user = await UserRepository().createUser(name=user.name, email=user.email, password=user.password)
        
        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail='Email already exists.'
        )

    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=500,
            detail='Internal server error. Try again later.'
        )
    
@user_router.put('/update', status_code=status.HTTP_200_OK)
async def update_user(user: UserUpdate):
    try:
        updated_user = await UserRepository().updateUserInfo(user.field, user.new_value, user.id)
        return updated_user
    
    except Exception as err:
        print(err)

        raise HTTPException(
            status_code=500,
            detail='Internal server error. Try again later.'
        )
    
@user_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_user(user: UserDelete):
    try:
        delted_user = await UserRepository().deleteUser(user.id)
        return delted_user
    
    except Exception as err:
        print(err)

        raise HTTPException(
            status_code=500,
            detail='Internal server error. Try again later.'
        )

