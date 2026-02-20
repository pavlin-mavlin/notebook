import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from controllers.commandcontroller import CommandController
from contextlib import suppress

class CommandEditDialog(tk.Toplevel):


    def __init__(self, parent,command_id=None):        
        super().__init__(parent)
        self.transient(parent)
        self.minsize(300, 150)
        self.title('Правка команды')
        self.resizable(0,0)
        self.result=messagebox.CANCEL
        with suppress(tk.TclError):
            self.attributes('-type', 'dialog')
        
        self.label_name = ttk.Label(self,text="Название: ",anchor=tk.E)
        self.label_name.grid(row=0, column=0, sticky='nsew')
        
        self.name_text = tk.StringVar()
        self.entry_name = ttk.Entry(self,textvariable = self.name_text)            
        self.name_text.trace("w", lambda *args: self.character_limit(255,self.name_text))
        self.entry_name.grid(row=0, column=1, sticky='nsew',padx=2, pady=2)
        
        self.label_command = ttk.Label(self,text="Команда: ",anchor=tk.E)
        self.label_command.grid(row=1, column=0, sticky='nsew')
        
        self.command_text = tk.StringVar()
        self.entry_command = ttk.Entry(self,textvariable = self.command_text)            
        self.command_text.trace("w", lambda *args: self.character_limit(255,self.command_text))
        self.entry_command.grid(row=1, column=1, sticky='nsew',padx=2, pady=2)
        
        self.is_default=tk.IntVar()
        self.check_default=ttk.Checkbutton(self,text="По умолчанию",variable=self.is_default)
        self.check_default.grid(row=2, column=1, sticky='nsew',padx=2, pady=2)       
        
        button_ok=ttk.Button(self, text="OK", command=self.on_OK)
        button_ok.grid(row=3,column=0)   
        
        button_cancel=ttk.Button(self, text="Отмена", command=self.destroy)
        button_cancel.grid(row=3,column=1)   
         
        
        if command_id:
            cc=CommandController()
            command=cc.get(command_id)
            self.name_text.set(command.name)
            self.command_text.set(command.command)
            self.is_default.set(command.default)

    def on_OK(self):
        self.result=tk.messagebox.OK
        self.quit()
        self.destroy()

    def character_limit(self,max_length,entry_text):
        if len(entry_text.get()) > max_length:
            entry_text.set(entry_text.get()[:max_length])            