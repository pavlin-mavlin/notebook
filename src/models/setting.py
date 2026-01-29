from peewee import CharField

from models.basemodel import BaseModel

class Setting(BaseModel):
    sname=CharField(primary_key = True)
    svalue=CharField()

  
        