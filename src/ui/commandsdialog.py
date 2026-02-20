import tkinter as tk
from tkinter import ttk

from controllers.commandcontroller import CommandController
from ui.commandeditdialog import CommandEditDialog
from models.command import Command
from tkinter import messagebox
from contextlib import suppress

class CommandsDialog(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.minsize(300, 150)
        self.title('Список команд')
        self.resizable(0,0)
        with suppress(tk.TclError):
            self.attributes('-type', 'dialog')
    
        self.list_frame = ttk.Frame(self)  
        self.listbox=tk.Listbox(self.list_frame,selectmode=tk.SINGLE,width=25)
        vsb = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)                
        self.list_frame.grid(column=0,rowspan=3)
        
        button_add=ttk.Button(self, text="Добавить",command=self.on_button_add)
        button_add.grid(row=0,column=1)
        
        button_edit=ttk.Button(self, text="Правка",command=self.on_button_edit)
        button_edit.grid(row=1,column=1)
        
        button_delete=ttk.Button(self, text="Удалить",command=self.on_button_delete)
        button_delete.grid(row=2,column=1)
        
        button_ok=ttk.Button(self, text="OK",command=self.destroy)
        button_ok.grid(row=3,column=0, columnspan=2)
                
        self.populate_list()
        
        
    def on_button_add(self):
        dialog = CommandEditDialog(self)
        dialog.mainloop() 
        if dialog.result == messagebox.OK:
            command=Command()
            command.name=dialog.name_text.get()
            command.command=dialog.command_text.get()
            command.default=dialog.is_default.get()
            cc=CommandController()
            cc.update(command)
            self.populate_list()                            
        
    def on_button_edit(self):
        sel=self.listbox.curselection()
        if sel:
            command_id=self.commandids[sel[0]]
            dialog = CommandEditDialog(self,command_id)
            dialog.mainloop() 
            if dialog.result == messagebox.OK:
                cc=CommandController()
                command=cc.get(command_id)
                command.name=dialog.name_text.get()
                command.command=dialog.command_text.get()
                command.default=dialog.is_default.get()
                cc.update(command)
                self.populate_list()                              
            
    def on_button_delete(self):
        sel=self.listbox.curselection()
        if sel:
            command_id=self.commandids[sel[0]]
            cc=CommandController()
            can_delete=cc.can_delete(command_id)
            if can_delete:
                result = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот элемент?",icon=messagebox.QUESTION)
                    
                if result == tk.YES:     
                    cc.delete(command_id)
                    self.populate_list()                
            else:                
                messagebox.showinfo("Сообщение", "Нельзя удалять эту команду")
            
    def populate_list(self):   
        self.listbox.delete(0, tk.END)     
        cc=CommandController()
        commands=cc.list()
        self.commandids=[]
        for command in commands:
            self.listbox.insert(tk.END,command.name)  
            self.commandids.append(command.command_id)  
                