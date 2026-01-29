from peewee import CharField,AutoField,ForeignKeyField
from models.node import Node
from models.basemodel import BaseModel
from models.command import Command

class Url(BaseModel):
    url_id = AutoField()   
    node_id = ForeignKeyField(Node, backref='urls',on_delete="CASCADE") 
    url = CharField(null=True)
    username = CharField(null=True)
    password = CharField(null=True)
    description = CharField(null=True)
    command_id=ForeignKeyField(Command,backref="commands",null=True)
    
    @staticmethod
    def get_db():
        return Url._meta.database    