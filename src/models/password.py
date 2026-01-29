from peewee import CharField,ForeignKeyField,AutoField, BooleanField
from models.basemodel import BaseModel
from models.node import Node

class Password(BaseModel):
    password_id = AutoField()   
    node_id = ForeignKeyField(Node, backref='passwords',on_delete="CASCADE") 
    username = CharField(null=True)
    password = CharField(null=True)
    description = CharField(null=True)
    pwencrypted = BooleanField(default=False)
