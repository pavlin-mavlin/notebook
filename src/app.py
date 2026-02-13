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
from tkinter import ttk
import argparse
 
class App(tk.Tk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Notebook")
        self.attributes('-zoomed', True)
        menu = tk.Menu(self)
        item = tk.Menu(menu, tearoff=0)        
        item.add_command(label='Команды',command=self.on_commands)
        item.add_command(label='Выход', command=self.quit)
        menu.add_cascade(label='Файл', menu=item)

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
        
        pw = tk.PanedWindow(orient ='horizontal')
        left_frame = NodesTree(self)
        left_frame.pack(side="left")
        pw.add(left_frame)
        right_frame = ttk.Frame(self)
        right_frame.pack(side="right")        
        pw.add(right_frame)
        
        pw.pack(fill = tk.BOTH, expand = True)
        pw.configure(sashrelief = tk.RAISED)
                
            
        
    def on_commands(self):
        pass        

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
