from models.memo import Memo

class MemoController(object):

    def __init__(self):
        '''
        Constructor
        '''

    def create_table(self):
        Memo.create_table()
        
    def get_by_node_id(self,node_id: int)->Memo:
        db_memo=Memo.select().where(Memo.node_id==node_id).get_or_none()
        return db_memo
    
    def update(self,db_memo: Memo):
        db_memo.save()
    
    def get(self,memo_id: int)->Memo:
        db_url=Memo.select().where(Memo.memo_id==memo_id).get_or_none()
        return db_url                     
    