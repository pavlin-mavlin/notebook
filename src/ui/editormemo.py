import tkinter as tk
from tkinter import ttk
from ui.editorinterface import EditorInterface
from controllers.memocontroller import MemoController
from models.memo import Memo

class EditorMemo(EditorInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.text_frame = ttk.Frame(self)        
        self.textview=tk.Text(self.text_frame)
        vsb = ttk.Scrollbar(self.text_frame, orient="vertical", command=self.textview.yview)
        self.textview.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        
        self.memo_id=None  
        self.show_all()

    def load_data(self, node_id: int):
        self.memo_id=None    
        if node_id!=-1:
            mc=MemoController()
            db_memo=mc.get_by_node_id(node_id)
            self.node_id=node_id
            
            if db_memo:
                self.textview.delete('1.0', tk.END)
                self.textview.insert(0,db_memo.memo)
                self.memo_id=db_memo.memo_id
    
    def save_data(self):
        mc=MemoController()
         
        if self.memo_id:
            db_memo=mc.get(self.memo_id)
        else:
            db_memo=Memo()
            db_memo.node_id=self.node_id
                
        db_memo.memo=self.textview.get(0)
        mc.update(db_memo)
        self.memo_id=db_memo.memo_id
                