from tortoise import models, fields

class Rating(models.Model):
    id = fields.IntField(pk=True)
    bad = fields.IntField()
    good = fields.IntField()
    great = fields.IntField()

    link = fields.ForeignKeyField(
        'models.Link',
        related_name='ratings',
        on_delete=fields.CASCADE
    )

