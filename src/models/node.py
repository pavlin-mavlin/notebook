from peewee import CharField,ForeignKeyField,AutoField, BooleanField,\
    IntegerField
from models.basemodel import BaseModel
from enum import Enum

class Node(BaseModel):
    node_id = AutoField()
    name = CharField()
    expanded = BooleanField()
    parent = ForeignKeyField('self', null=True, backref='children')
    type = IntegerField()
    weight=IntegerField(default=0)


class NodeType(Enum):
    FOLDER=1
    MEMO=2
    PASSWORD=3
    URL=4
    
    