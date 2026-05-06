from pydantic import BaseModel, constr, conint

class LinkCreate(BaseModel):
    name: constr(min_length=1, strip_whitespace=True)
    user_id: conint()

class LinkUpdateName(BaseModel):
    link_id: conint()
    new_name: constr(min_length=1, strip_whitespace=True)

class LinkUpdateRating(BaseModel):
    link_id: constr(min_length=1, strip_whitespace=True)
    rating: constr(min_length=1, strip_whitespace=True)