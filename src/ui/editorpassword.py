import tkinter as tk
from tkinter import ttk
from ui.editorinterface import EditorInterface
from controllers.passwordcontroller import PasswordController
from models.password import Password

class EditorPassword(EditorInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                        
        self.okimage=tk.PhotoImage(file="images/2714-green.png")
        
        self.frame_fields=ttk.Frame(self)
        
        self.label_username = ttk.Label(self.frame_fields,text="Имя пользователя: ",anchor=tk.E)
        self.label_username.grid(row=0, column=0, sticky='nsew')
        
        self.image_copy=tk.PhotoImage(file="images/copy.png")
        self.button_username_copy=ttk.Button(self.frame_fields,image=self.image_copy, command=self.on_username_copy)         
        self.button_username_copy.grid(row=0, column=1,padx=2, pady=2)
        
        self.username_text = tk.StringVar()
        self.entry_username = ttk.Entry(self.frame_fields,textvariable = self.username_text)            
        self.username_text.trace("w", lambda *args: self.character_limit(255,self.username_text))
        self.entry_username.grid(row=0, column=2, sticky='nsew',padx=2, pady=2)
        
        self.label_password=ttk.Label(self.frame_fields,text="Пароль: ",anchor=tk.E)
        self.label_password.grid(row=1, column=0, sticky='nsew')
        
        self.button_password_copy=ttk.Button(self.frame_fields,image=self.image_copy, command=self.on_password_copy)  
        self.button_password_copy.grid(row=1, column=1,padx=2, pady=2)
        
        self.password_text = tk.StringVar()
        self.entry_password = ttk.Entry(self.frame_fields,textvariable = self.password_text,show="•")
        self.password_text.trace("w", lambda *args: self.character_limit(255,self.password_text))
        self.entry_password.grid(row=1, column=2, sticky='nsew',padx=2, pady=2)
        
        self.image_password_show=tk.PhotoImage(file="images/2a-20e3.png")
        self.button_password_show=ttk.Button(self.frame_fields,image=self.image_password_show, command=self.on_password_show) 
        self.button_password_show.grid(row=1, column=3)

        self.frame_fields.grid_columnconfigure(2, weight=1,pad=3)        
        self.frame_fields.pack(side=tk.TOP, fill=tk.X)
                        
        self.label_description=ttk.Label(self,text="Описание",anchor=tk.CENTER)
        self.label_description.pack(side=tk.TOP, fill=tk.X)
        
        self.text_frame = ttk.Frame(self)        
        self.textview=tk.Text(self.text_frame)
        vsb = ttk.Scrollbar(self.text_frame, orient="vertical", command=self.textview.yview)
        self.textview.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.pack(side=tk.TOP, fill=tk.BOTH,expand=1)
                
    def load_data(self, node_id: int):
        self.password_id=None    
        if node_id!=-1:
            pc=PasswordController()
            db_password=pc.get_by_node_id(node_id)
            self.node_id=node_id
            
            if db_password:
                self.username_text.set(db_password.username)
                self.password_text.set(db_password.password)     
                self.textview.delete('1.0', tk.END)           
                self.textview.insert('1.0',db_password.description)
                self.password_id=db_password.password_id
    
    def save_data(self):
        pc=PasswordController()
         
        if self.password_id:
            db_password=pc.get(self.password_id)
        else:
            db_password=Password()
            db_password.node_id=self.node_id
        
        db_password.username=self.username_text.get()
        
        if self.entry_password.cget("show")=="•":
            db_password.password=self.password_text.get()
            
        db_password.description=self.textview.get("1.0",tk.END)
        pc.update(db_password)
        self.password_id=db_password.password_id
    
    def on_username_copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.username_text.get())      
        self.button_username_copy.config(image=self.okimage)
        self.update_idletasks()
        self.after(3000, self.restore_image(self.button_username_copy))
        
    def on_password_copy(self):
        self.clipboard_clear()
        if self.entry_password.cget("show")=="•":
            pc=PasswordController()
            db_password=pc.get(self.password_id)
            self.clipboard_append(db_password.password)
        else:
            self.clipboard_append(self.password_text.get())     

        self.button_password_copy.config(image=self.okimage)
        self.update_idletasks()
        self.after(3000, self.restore_image(self.button_password_copy))
        
    def on_password_show(self):
        if self.entry_password.cget("show")=="•":
            self.entry_password.config(show="")      
        else:
            self.entry_password.config(show="•")

    def character_limit(self,max_length,entry_text):
        if len(entry_text.get()) > max_length:
            entry_text.set(entry_text.get()[:max_length])
    

        