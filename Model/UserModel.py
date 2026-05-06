from tortoise import models, fields

class User(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    email = fields.CharField(max_length=255, null=False, unique=True)
    password = fields.CharField(max_length=12, min_length=8, null=False)
    
    links: fields.ReverseRelation['Link']
    