from models.setting import Setting

class SettingController(object):

    def __init__(self):
        '''
        Constructor
        '''

    def create_table(self):
        Setting.create_table()     
        
    def get(self,setting_name)->Setting:
        db_setting=Setting.select().where(Setting.sname==setting_name).get_or_none()
        return db_setting
    
    def update(self,setting_name,setting_value):
        db_setting=self.get(setting_name)
        force_insert=db_setting is None #без этого он не знает когда обновлять когда добавлять запись
        
        if db_setting is None:
            db_setting=Setting()
            db_setting.sname=setting_name                        
        
        db_setting.svalue=setting_value
        db_setting.save(force_insert)
        
    