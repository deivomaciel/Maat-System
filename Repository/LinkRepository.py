from Model.LinkModel import Link
from Model.RatingModel import Rating
from tortoise.expressions import F


class LinkRepository():

    async def createLink(self, name: str, user_id: int):
        link = Link(name=name, user_id=user_id)
        await link.save()
        initial_rating = Rating(bad=0, good=0, great=0, link_id=link.id)
        await initial_rating.save()
        return link

    async def getLinksByUserId(self, user_id: int):
        # Use the known user_id directly to avoid FK attribute ambiguity
        links = await Link.filter(user_id=user_id).all()
        result = []
        for link in links:
            rating = await Rating.get_or_none(link_id=link.id)
            bad = rating.bad if rating else 0
            good = rating.good if rating else 0
            great = rating.great if rating else 0
            result.append({
                "id": link.id,
                "name": link.name,
                "user_id": user_id,
                "bad": bad,
                "good": good,
                "great": great,
                "total": bad + good + great,
            })
        return result

    async def getLinkWithRating(self, link_id: int, user_id: int):
        # Filter by both id and user_id to enforce ownership in the query
        link = await Link.filter(id=link_id, user_id=user_id).first()
        if not link:
            return None
        rating = await Rating.get_or_none(link_id=link_id)
        bad = rating.bad if rating else 0
        good = rating.good if rating else 0
        great = rating.great if rating else 0
        return {
            "id": link.id,
            "name": link.name,
            "user_id": user_id,
            "bad": bad,
            "good": good,
            "great": great,
            "total": bad + good + great,
        }

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
                await Rating.filter(link_id=link_id).update(bad=F('bad') + 1)
            case 'good':
                await Rating.filter(link_id=link_id).update(good=F('good') + 1)
            case 'great':
                await Rating.filter(link_id=link_id).update(great=F('great') + 1)
            case _:
                return False
        if link_rating:
            await link_rating.refresh_from_db()
        return link_rating
