import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

from controllers.commandcontroller import CommandController
from ui.commandeditdialog import CommandEditDialog
from models.command import Command
from tkinter import messagebox

class CommandsDialog(simpledialog.Dialog):

    def body(self, parent):
        self.main_frame= ttk.Frame(self) 
           
        self.list_frame = ttk.Frame(self.main_frame)  
        self.listbox=tk.Listbox(self.list_frame,selectmode=tk.SINGLE,width=25)
        vsb = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)                
        self.list_frame.grid(column=0,rowspan=3)
        
        button_add=ttk.Button(self.main_frame, text="Добавить",command=self.on_button_add)
        button_add.grid(row=0,column=1)
        
        button_edit=ttk.Button(self.main_frame, text="Правка",command=self.on_button_edit)
        button_edit.grid(row=1,column=1)
        
        button_delete=ttk.Button(self.main_frame, text="Удалить",command=self.on_button_delete)
        button_delete.grid(row=2,column=1)
        
        self.main_frame.pack()
        self.populate_list()
        
        return self.listbox
        
    def on_button_add(self):
        dialog = CommandEditDialog(self)        
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
    
    def buttonbox(self):
        box = ttk.Frame(self)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)

        box.pack()                