import tkinter as tk
from tkinter import ttk

from controllers.commandcontroller import CommandController
from ui.commandeditdialog import CommandEditDialog
from models.command import Command
from tkinter import messagebox

class CommandsDialog(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.minsize(300, 150)
        self.title('Список команд')
        self.resizable(0,0)
                
        self.list_frame = ttk.Frame(self)  
        self.listbox=tk.Listbox(self.list_frame,selectmode=tk.SINGLE)
        vsb = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)                
        self.list_frame.grid(column=0,rowspan=3)
        
        button_add=ttk.Button(self, text="Добавить")
        button_add.grid(row=0,column=1)
        
        button_edit=ttk.Button(self, text="Правка")
        button_edit.grid(row=1,column=1)
        
        button_delete=ttk.Button(self, text="Удалить")
        button_delete.grid(row=2,column=1)
        
        button_ok=ttk.Button(self, text="OK",command=self.destroy)
        button_ok.grid(row=3,column=1)
                
        self.populate_list()
        
        
    def on_button_add(self, widget):
        dialog = CommandEditDialog(self)
        response=dialog.run()
        if response == "OK":
            command=Command()
            command.name=dialog.entry_name.get_text()
            command.command=dialog.entry_command.get_text()
            command.default=dialog.check_default.get_active()
            cc=CommandController()
            cc.update(command)
            self.populate_list()
                            
        dialog.destroy() 
        
    def on_button_edit(self,widget):
        row=self.listbox.get_selected_row()
        if row:
            dialog = CommandEditDialog(self,row.command_id)
            response=dialog.run()
            if response == "OK":
                cc=CommandController()
                command=cc.get(row.command_id)
                command.name=dialog.entry_name.get_text()
                command.command=dialog.entry_command.get_text()
                command.default=dialog.check_default.get_active()
                cc.update(command)
                self.populate_list()
                                
            dialog.destroy() 
            
    def on_button_delete(self,widget):
        row=self.listbox.get_selected_row()
        if row:
            cc=CommandController()
            can_delete=cc.can_delete(row.command_id)
            if can_delete:
                result = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот элемент?",icon=tk.messagebox.QUESTION)
                    
                if result == tk.YES:     
                    cc.delete(row.command_id)
                    self.populate_list()                
            else:                
                messagebox.showinfo("Сообщение", "Нельзя удалять эту команду")
            
    def populate_list(self):        
        cc=CommandController()
        commands=cc.list()
        self.commandids=[]
        for command in commands:
            self.listbox.insert(tk.END,command.name)  
            self.commandids.append(command.command_id)  
                