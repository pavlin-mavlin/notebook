from models.basemodel import BaseModel
from peewee import AutoField, CharField, BooleanField

class Command(BaseModel):
    command_id=AutoField()
    name=CharField()
    command=CharField()
    default=BooleanField(default=False)
