import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

from controllers.commandcontroller import CommandController

class CommandEditDialog(simpledialog.Dialog):

    def __init__(self, parent,command_id=None): 
        self.command_id=command_id
        self.result=messagebox.CANCEL
        super().__init__(parent, "Создание/редактирование команды")                
    
    def body(self, parent):        

        self.main_frame = ttk.Frame(self)             
        self.label_name = ttk.Label(self.main_frame,text="Название: ",anchor=tk.E)
        self.label_name.grid(row=0, column=0, sticky='nsew')
        
        self.name_text = tk.StringVar()
        self.entry_name = ttk.Entry(self.main_frame,textvariable = self.name_text)            
        self.name_text.trace("w", lambda *args: self.character_limit(255,self.name_text))
        self.entry_name.grid(row=0, column=1, sticky='nsew',padx=2, pady=2)
        
        self.label_command = ttk.Label(self.main_frame,text="Команда: ",anchor=tk.E)
        self.label_command.grid(row=1, column=0, sticky='nsew')
        
        self.command_text = tk.StringVar()
        self.entry_command = ttk.Entry(self.main_frame,textvariable = self.command_text)            
        self.command_text.trace("w", lambda *args: self.character_limit(255,self.command_text))
        self.entry_command.grid(row=1, column=1, sticky='nsew',padx=2, pady=2)
        
        self.is_default=tk.IntVar()
        self.check_default=ttk.Checkbutton(self.main_frame,text="По умолчанию",variable=self.is_default)
        self.check_default.grid(row=2, column=1, sticky='nsew',padx=2, pady=2)    
        self.main_frame.pack()         
        
        if self.command_id:
            cc=CommandController()
            command=cc.get(self.command_id)
            self.name_text.set(command.name)
            self.command_text.set(command.command)
            self.is_default.set(command.default)
            
        return self.entry_name

    def character_limit(self,max_length,entry_text):
        if len(entry_text.get()) > max_length:
            entry_text.set(entry_text.get()[:max_length])     
            
    def apply(self)->None:
        self.result=messagebox.OK
