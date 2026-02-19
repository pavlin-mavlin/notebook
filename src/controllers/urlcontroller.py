from models.url import Url
from models.command import Command


class UrlController(object):

    def __init__(self):
        '''
        Constructor
        '''
        
    def create_table(self):
        Url.create_table()
        
#    def get_by_node_id(self,node_id: int)->Url:
#        db_url=(Url.select(Url.url_id,Url.url,Command.name,Url.username,Url.password,Url.description).join(Command).where(Url.node_id==node_id).dicts())
#        return db_url
    
    def update(self,db_url: Url):
        db_url.save()
    
    def get(self,url_id: int)->Url:
        db_url=Url.select().where(Url.url_id==url_id).get_or_none()
        return db_url
    