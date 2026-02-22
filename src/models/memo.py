from peewee import TextField,AutoField,ForeignKeyField
from models.node import Node
from models.basemodel import BaseModel

class Memo(BaseModel):
    memo_id = AutoField()   
    node_id = ForeignKeyField(Node, backref='memos',on_delete="CASCADE") 
    memo = TextField(null=True)

