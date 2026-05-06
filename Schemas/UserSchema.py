from pydantic import BaseModel, constr, EmailStr, conint, conlist

class UserCreate(BaseModel):
    name: constr(min_length=1, strip_whitespace=True)
    email: EmailStr
    password: constr(max_length=8)

class UserUpdate(BaseModel):
    id: conint()
    field: constr(min_length=1, strip_whitespace=True)
    new_value: constr(min_length=1, strip_whitespace=True)

class UserDelete(BaseModel):
    id: conint()