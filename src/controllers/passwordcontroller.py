from models.password import Password

class PasswordController(object):
    def __init__(self):
        '''
        Constructor
        '''

    def create_table(self): 
        Password.create_table()      
    
    def get_by_node_id(self,node_id: int)->Password:
        password=Password.select().where(Password.node_id==node_id).get_or_none()
        return password
    
    def update(self,password: Password):
        password.save()
    
    def get(self,password_id: int)->Password:
        password=Password.select().where(Password.password_id==password_id).get_or_none()
        return password
    
    