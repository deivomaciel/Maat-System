from Model.LinkModel import Link 
from Model.RatingModel import Rating
from tortoise.expressions import F

class LinkRepository():

    async def createLink(self, name: str, user_id: int):
        link = await Link(name=name, user_id=user_id)
        await link.save()

        inital_rating = Rating(bad=0, good=0, great=0, link_id=link.id)
        await inital_rating.save()

        return link
    
    async def updateLinkName(self, link_id: int, new_name: str):
        link = await Link.get_or_none(id=link_id)

        if link:
            setattr(link, 'name', new_name)
            await link.save()

        return link
    
    async def deletLink(self, link_id: int):
        link = await Link.get_or_none(id=link_id)

        if link:
            await link.delete()
            
        return link

    async def updateLinkRating(self, link_id: int, rating: str):
        link_rating = await Rating.get_or_none(link_id=link_id)
        

        match rating:
            case 'bad':
                await Rating.filter(link_id=link_id).update(
                    bad=F('bad') + 1
                )

            case 'good':
                await Rating.filter(link_id=link_id).update(
                    good=F('good') + 1
                )

            case 'great':
                await Rating.filter(link_id=link_id).update(
                    great=F('great') + 1
                )

            case _:
                return False

        await link_rating.refresh_from_db()
        return link_rating
    
    async def getLinksByUser(self, user_id: int):
        links = await Link.filter(user_id=user_id).all()
        return links
    
    async def getLinkRating(self, link_id: int):
        return await Rating.get_or_none(link_id=link_id)

