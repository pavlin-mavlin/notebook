import tkinter as tk
from tkinter import ttk
from controllers.commandcontroller import CommandController
from ui.editorinterface import EditorInterface
from controllers.urlcontroller import UrlController
from models.url import Url 
import subprocess
from tkinter import messagebox

class EditorUrl(EditorInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        self.okimage=tk.PhotoImage(file="images/2714-green.png")
        
        self.frame_fields=ttk.Frame(self)
        
        self.label_url = ttk.Label(self.frame_fields,text="URL ссылка: ",anchor=tk.E)
        self.label_url.grid(row=0, column=0, sticky='nsew')
        
        self.image_copy=tk.PhotoImage(file="images/copy.png")
        self.button_url_copy=ttk.Button(self.frame_fields,image=self.image_copy, command=self.on_url_copy)  
        self.button_url_copy.grid(row=0, column=1,padx=2, pady=2)
        
        self.url_frame=ttk.Frame(self.frame_fields)                     
        
        self.url_text = tk.StringVar()
        self.entry_url = ttk.Entry(self.url_frame,textvariable = self.url_text) 
        self.url_text.trace("w", lambda *args: self.character_limit(255,self.url_text))
        self.entry_url.grid(row=0, column=0,sticky='nsew')
                
        cc=CommandController() 
        arcn=[]       
        self.commandids=[] #combobox не поддерживает хранение значения, но его можно хранить в отдельном массиве с совпадающими индексами
        commands=cc.list()
        for command in commands:
            arcn.append(command.name)
            self.commandids.append(command.command_id)
                
        self.combo_command = ttk.Combobox(self.url_frame,state="readonly",values=arcn)
        self.combo_command.grid(row=0, column=1)
        
        default_command=cc.get_default()
        if default_command:
            self.combo_command.set(default_command.name)
        
        self.url_frame.grid_columnconfigure(0, weight=1)
        self.url_frame.grid_rowconfigure(0, weight=1)
        self.url_frame.grid(row=0, column=2, sticky='nsew',padx=2, pady=2)

        self.open_image=tk.PhotoImage(file="images/25b6.png")
        self.button_url_open=ttk.Button(self.frame_fields,image=self.open_image,command=self.on_url_open)
        self.button_url_open.grid(row=0, column=3,padx=2, pady=2)
                
        self.label_username = ttk.Label(self.frame_fields,text="Имя пользователя: ",anchor=tk.E)
        self.label_username.grid(row=1, column=0, sticky='nsew')        
                
        self.button_username_copy=ttk.Button(self.frame_fields,image=self.image_copy, command=self.on_username_copy)         
        self.button_username_copy.grid(row=1, column=1,padx=2, pady=2)
                
        self.username_text = tk.StringVar()
        self.entry_username = ttk.Entry(self.frame_fields,textvariable = self.username_text)            
        self.username_text.trace("w", lambda *args: self.character_limit(255,self.username_text))
        self.entry_username.grid(row=1, column=2, sticky='nsew',padx=2, pady=2)
        
        self.label_password=ttk.Label(self.frame_fields,text="Пароль: ",anchor=tk.E)
        self.label_password.grid(row=2, column=0, sticky='nsew')
        
        self.button_password_copy=ttk.Button(self.frame_fields,image=self.image_copy, command=self.on_password_copy)  
        self.button_password_copy.grid(row=2, column=1,padx=2, pady=2)
        
        self.password_text = tk.StringVar()
        self.entry_password = ttk.Entry(self.frame_fields,textvariable = self.password_text,show="•")
        self.password_text.trace("w", lambda *args: self.character_limit(255,self.password_text))
        self.entry_password.grid(row=2, column=2, sticky='nsew',padx=2, pady=2)
        
        self.image_password_show=tk.PhotoImage(file="images/2a-20e3.png")
        self.button_password_show=ttk.Button(self.frame_fields,image=self.image_password_show, command=self.on_password_show) 
        self.button_password_show.grid(row=2, column=3,padx=2, pady=2)
        
        self.frame_fields.grid_columnconfigure(2, weight=1,pad=3)
        
        self.frame_fields.pack(side=tk.TOP, fill=tk.X)
        
        self.label_description=ttk.Label(self,text="Описание",anchor=tk.CENTER)
        self.label_description.pack(side=tk.TOP, fill=tk.X)
        
        
        self.text_frame = tk.Frame(self)        
        self.textview=tk.Text(self.text_frame)
        vsb = ttk.Scrollbar(self.text_frame, orient="vertical", command=self.textview.yview)
        self.textview.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.pack(side=tk.TOP, fill=tk.BOTH,expand=1)

    def load_data(self, node_id: int):
        self.url_id=None    
        if node_id!=-1:
            uc=UrlController()
            db_url=uc.get_by_node_id(node_id)
            self.node_id=node_id
            
            if db_url:
                self.url_text.set(db_url.url)
                if db_url.command_id:
                    i=self.commandids.index(db_url.command_id.command_id)
                    self.combo_command.current(i)
                
                self.username_text.set(db_url.username)
                self.password_text.set(db_url.password)                
                self.textview.delete('1.0', tk.END)   
                self.textview.insert('1.0',db_url.description)
                self.url_id=db_url.url_id
    
    def save_data(self):
        uc=UrlController()
         
        if self.url_id:
            db_url=uc.get(self.url_id)
        else:
            db_url=Url()
            db_url.node_id=self.node_id
        
        db_url.url=self.url_text.get()

        i=self.combo_command.current()
        db_url.command_id=self.commandids[i]
        
        db_url.username=self.username_text.get()
        
        if self.entry_password.cget("show")=="•":
            db_url.password=self.password_text.get()
            
        db_url.description=self.textview.get("1.0",tk.END)
        uc.update(db_url)
        self.url_id=db_url.url_id        
            
    def on_url_open(self):
        i=self.combo_command.current()       
        url=self.url_text.get()
                         
        if i!=-1 and url:
            command_id=self.commandids[i]
            cc=CommandController()
            command=cc.get(command_id)
            if command.command:
                subprocess.Popen([command.command, url])
            else:
                urlparts=url.split()
                subprocess.Popen(urlparts)
        else:            
            messagebox.showinfo("Уведомление", "Нет команды или ссылки")
            
    def on_username_copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.username_text.get())        
        self.button_username_copy.config(image=self.okimage)
        self.update_idletasks()
        self.after(1000, self.restore_image(self.button_username_copy))
        
    def on_password_copy(self):        
        self.clipboard_clear()
        if self.entry_password.cget("show")=="•":
            uc=UrlController()
            db_url=uc.get(self.url_id)
            self.clipboard_append(db_url.password)
        else:
            self.clipboard_append(self.password_text.get())     

        self.button_password_copy.config(image=self.okimage)
        self.update_idletasks()
        self.after(1000, self.restore_image(self.button_password_copy))        

    def on_password_show(self):
        if self.entry_password.cget("show")=="•":
            self.entry_password.config(show="")      
        else:
            self.entry_password.config(show="•")

    def on_url_copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.url_text.get())
        self.button_url_copy.config(image=self.okimage)
        self.update_idletasks()
        self.after(1000, self.restore_image(self.button_url_copy))           

    def character_limit(self,max_length,entry_text):
        if len(entry_text.get()) > max_length:
            entry_text.set(entry_text.get()[:max_length])        
