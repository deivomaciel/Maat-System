from fastapi import APIRouter, status, HTTPException
from Schemas.LinkSchema import LinkCreate, LinkUpdateName, LinkUpdateRating
from Repository.LinkRepository import LinkRepository

link_router = APIRouter(prefix='/link', tags=['Link'])

@link_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_link(link: LinkCreate):
    try:
        new_link = await LinkRepository().createLink(link.name, link.user_id)
        return new_link

    except Exception as err:
        print(err)

        raise HTTPException(
            status_code=500,
            detail='Internal server error. Try again later.'
        )
    
@link_router.put('/update', status_code=status.HTTP_200_OK)
async def update_name(link: LinkUpdateName):
    try:
        updated_link = await LinkRepository().updateLinkName(link.link_id, link.new_name)
        return updated_link

    except Exception as err:
        print(err)

        raise HTTPException(
            status_code=500,
            detail='Internal server error. Try again later.'
        )
    
@link_router.get('/rating/{link_id}/{rating}', status_code=status.HTTP_200_OK)
async def update_name(link_id: int, rating: str):
    try:
        await LinkRepository().updateLinkRating(link_id, rating)
        return {
            "message": "ok"
        }

    except Exception as err:
        print(err)

        raise HTTPException(
            status_code=500,
            detail='Internal server error. Try again later.'
        )
    
@link_router.get('/all/{user_id}', status_code=status.HTTP_200_OK)
async def get_link_by_user(user_id: int):
    try:
        links = await LinkRepository().getLinksByUser(user_id)
        return links

    except Exception as err:
        print(err)

        raise HTTPException(
            status_code=500,
            detail='Internal server error. Try again later.'
        )
    
@link_router.get('/get-rating/{link_id}', status_code=status.HTTP_200_OK)
async def get_link_rating(link_id: int):
    try:
        rating = await LinkRepository().getLinkRating(link_id)
        return rating

    except Exception as err:
        print(err)

        raise HTTPException(
            status_code=500,
            detail='Internal server error. Try again later.'
        )