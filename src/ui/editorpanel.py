import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.node import NodeType
from ui.editorurl import EditorUrl
from ui.editormemo import EditorMemo
from ui.editorpassword import EditorPassword

class EditorPanel(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        toolbar=ttk.Frame(self, borderwidth = 1, relief=tk.RAISED)
        
        self.image_save=tk.PhotoImage(file="images/1f4be.png")
        self.button_save=ttk.Button(toolbar,image=self.image_save, state=tk.DISABLED,width=34,command=self.on_save) 
        self.button_save.pack(side=tk.LEFT, padx=2, pady=5)
                
        self.image_revert=tk.PhotoImage(file="images/revert.png")
        self.button_revert=ttk.Button(toolbar,image=self.image_revert, state=tk.DISABLED,width=34,command=self.on_revert)
        self.button_revert.pack(side=tk.LEFT, padx=2, pady=5)
        
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.editor=None
        self.node_id=None
        self.node_type=None
        
        self.editors={NodeType.URL.value: EditorUrl, 
                      NodeType.MEMO.value: EditorMemo,
                      NodeType.PASSWORD.value: EditorPassword}
           
    def on_node_changed(self,node_id: int,node_type: int):        
        if self.editor:
            self.editor.save_data()
            self.editor.destroy()
            self.editor=None
            self.button_save.config(state=tk.DISABLED)
            self.button_revert.config(state=tk.DISABLED)      

        self.node_id=node_id
        self.node_type=node_type

        if self.node_id and self.node_id!=-1 and self.editors.get(self.node_type,None):      
            self.editor=self.editors[self.node_type](self,borderwidth = 1, relief=tk.RAISED)   
            if self.editor:            
                self.button_save.config(state=tk.NORMAL)
                self.button_revert.config(state=tk.NORMAL)               
                self.editor.load_data(self.node_id)    
                self.editor.pack(side=tk.TOP, fill=tk.BOTH,expand=1)         
                        
    def on_node_edited(self,node_id: int,node_type: int):        
        if self.editor:
            self.on_save()
            
        self.node_id=node_id
        self.node_type=node_type
        
        if not self.editor:
            self.editor=self.editors[self.node_type](self)
            if self.editor:
                self.button_save.config(state=tk.NORMAL)
                self.button_revert.config(state=tk.NORMAL)
                self.editor.load_data(self.node_id)
                self.editor.pack(side=tk.TOP, fill=tk.BOTH,expand=1)        
    
    def on_save(self):
        if self.editor and self.node_id:
            self.editor.save_data()
            
    def on_revert(self):
        if self.editor and self.node_id:            
            result = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите отменить изменения?",icon=tk.messagebox.QUESTION)
            
            if result == tk.YES:
                self.editor.load_data(self.node_id)
            
