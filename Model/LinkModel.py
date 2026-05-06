from tortoise import models, fields

class Link(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    token = fields.CharField(max_length=255, null=False, unique=True)

    user = fields.ForeignKeyField(
        'models.User',
        related_name='links',
        on_delete=fields.CASCADE
    )