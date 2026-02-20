import tkinter as tk

class EditorInterface(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def load_data(self, node_id: int):
        pass
    
    def save_data(self):
        pass    

    def restore_image(self,button):
        button.config(image=self.image_copy)