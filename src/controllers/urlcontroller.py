from models.url import Url


class UrlController(object):

    def __init__(self):
        '''
        Constructor
        '''
        
    def create_table(self):
        Url.create_table()
        
    def get_by_node_id(self,node_id: int)->Url:
        db_url=Url.select().where(Url.node_id==node_id).get_or_none()
        return db_url
    
    def update(self,db_url: Url):
        db_url.save()
    
    def get(self,url_id: int)->Url:
        db_url=Url.select().where(Url.url_id==url_id).get_or_none()
        return db_url
    