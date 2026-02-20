from models.basemodel import database
from controllers.nodecontroller import NodeController
from controllers.urlcontroller import UrlController
from controllers.memocontroller import MemoController
from controllers.passwordcontroller import PasswordController
from controllers.settingcontroller import SettingController
from controllers.commandcontroller import CommandController
from ui.commandsdialog import CommandsDialog
from ui.nodestree import NodesTree
import tkinter as tk
import argparse
from ui.editorpanel import EditorPanel
 
class App(tk.Tk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Notebook")
        self.attributes('-zoomed', True)
        menu = tk.Menu(self)
        item = tk.Menu(menu, tearoff=0)        
        item.add_command(label='Команды',command=self.on_commands)
        item.add_command(label='Выход', command=self.destroy)
        menu.add_cascade(label='Файл', menu=item)
        self['menu'] = menu
        
        icon = tk.PhotoImage(file = 'images/1f4d4.png')
        self.wm_iconphoto(True, icon)

        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--database", help="set database path")
        args = parser.parse_args()
        database_path=args.database
    
        if not database_path:
            database_path="notebook.db"
            
        database.init(database_path)
        
        nc=NodeController()
        nc.create_table()
        nc.create_root()
        #create other tables here by calling their controller
        UrlController().create_table()
        MemoController().create_table()
        PasswordController().create_table()
        SettingController().create_table()
        CommandController().create_table()
        
        self.pw = tk.PanedWindow(orient =tk.HORIZONTAL)
        self.left_frame = NodesTree(self)
        self.left_frame.pack(side=tk.LEFT)
        self.pw.add(self.left_frame)
        self.right_frame = EditorPanel(self)
        self.right_frame.pack(side=tk.RIGHT)        
        self.pw.add(self.right_frame)
        self.left_frame.subscriber=self.right_frame
                
        self.pw.pack(fill = tk.BOTH, expand = True)
        self.pw.configure(sashrelief = tk.RAISED)
        #self.right_frame.bind("<Destroy>",lambda event: self.on_panedwindow_destroyed(event))           
        
        self.update_idletasks() #без этого sash_place не работает
        sc=SettingController()
        setting=sc.get("paned_position")
        if setting and setting.svalue:            
            self.pw.sash_place(0,int(setting.svalue),0)
    
    def destroy(self)->None:
        self.right_frame.on_save()
        #сохранить позицию разделителя
        sc=SettingController()
        x,y=self.pw.sash_coord(0)
        sc.update("paned_position", x)        
        
        super().destroy()
        self.quit()
    
    def on_commands(self):
        CommandsDialog(self,'Список команд')           
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
