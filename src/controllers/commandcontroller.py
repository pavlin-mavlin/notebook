from models.command import Command
from models.url import Url

class CommandController(object):

    def __init__(self):
        '''
        Constructor
        '''
        
    def create_table(self):
        Command.create_table()    
        commands=self.list()
        if commands.count()==0:
            command=Command()
            command.name="выполнить"
            command.command=""
            self.update(command)    
            
    def list(self):
        return Command.select()                    
    
    def update(self,command: Command):
        command.save()
    
    def get(self,command_id):
        return Command.select().where(Command.command_id==command_id).get_or_none()
    
#    def get_by_name(self,name):
#        return Command.select().where(Command.name==name).get_or_none()
    
    def delete(self,command_id):
        Command.delete_by_id(command_id)
    
    def can_delete(self,command_id):
        return not Url.select().where(Url.command_id==command_id).exists()
    
    def get_default(self):
        return Command.select().where(Command.default==True).get_or_none()