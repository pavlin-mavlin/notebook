from peewee import Model,SqliteDatabase

database=SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = database
    

    
        