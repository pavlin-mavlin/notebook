import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from ui.editorinterface import EditorInterface
from controllers.passwordcontroller import PasswordController
from models.password import Password
import ui

class EditorPassword(EditorInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.set_orientation(Gtk.Orientation.VERTICAL)
        
        grid = Gtk.Grid(border_width=10,row_spacing=10,column_spacing=10)
        
        label_username = Gtk.Label(label="Имя пользователя: ")
        grid.add(label_username)
        
        self.button_username_copy=Gtk.Button.new_from_icon_name("edit-copy",Gtk.IconSize.BUTTON)
        self.button_username_copy.connect("clicked",self.on_username_copy)
        grid.attach(self.button_username_copy,1,0,1,1)
        
        self.entry_username = Gtk.Entry(hexpand=True)
        self.entry_username.set_max_length(255) 
        grid.attach_next_to(self.entry_username,self.button_username_copy,Gtk.PositionType.RIGHT,1,1)
        
        label_password=Gtk.Label(label="Пароль: ",xalign=1)
        grid.attach(label_password,0,1,1,1)
        
        self.button_password_copy=Gtk.Button.new_from_icon_name("edit-copy",Gtk.IconSize.BUTTON)
        self.button_password_copy.connect("clicked",self.on_password_copy)
        grid.attach(self.button_password_copy,1,1,1,1)
        
        self.entry_password = Gtk.Entry(hexpand=True)
        self.entry_password.set_max_length(255)    
        grid.attach_next_to(self.entry_password,self.button_password_copy,Gtk.PositionType.RIGHT,1,1)
        
        image_password_show=ui.get_scaled_image("2a-20e3.svg")
        button_password_show=Gtk.Button(image=image_password_show)
        button_password_show.connect("clicked",self.on_password_show)
        grid.attach_next_to(button_password_show,self.entry_password,Gtk.PositionType.RIGHT,1,1)    

        self.add(grid)
        
        label_description=Gtk.Label(label="Описание")
        self.add(label_description)
        
        scrolledwindow = Gtk.ScrolledWindow(border_width=10)
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()        
        scrolledwindow.add(self.textview)
        self.add(scrolledwindow)
        
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        
        self.show_all()
        
    def load_data(self, node_id: int):
        self.password_id=None    
        if node_id!=-1:
            pc=PasswordController()
            db_password=pc.get_by_node_id(node_id)
            self.node_id=node_id
            
            if db_password:
                self.entry_username.set_text(db_password.username)
                self.entry_password.set_text(ui.make_password_placeholder(db_password.password))
                textbuffer = self.textview.get_buffer()
                textbuffer.set_text(db_password.description)
                self.password_id=db_password.password_id
    
    def save_data(self):
        pc=PasswordController()
         
        if self.password_id:
            db_password=pc.get(self.password_id)
        else:
            db_password=Password()
            db_password.node_id=self.node_id
        
        db_password.username=self.entry_username.get_text()
        
        if "•" not in self.entry_password.get_text():
            db_password.password=self.entry_password.get_text()
            
        textbuffer = self.textview.get_buffer()
        db_password.description=textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(),True)
        pc.update(db_password)
        self.password_id=db_password.password_id
    
    def on_username_copy(self, widget):
        self.clipboard.set_text(self.entry_username.get_text(), -1)
        okimage=ui.get_scaled_image("2714-green.svg")
        self.button_username_copy.set_image(okimage)
        
    def on_password_copy(self, widget):
        if "•" in self.entry_password.get_text():
            pc=PasswordController()
            db_password=pc.get(self.password_id)
            self.clipboard.set_text(db_password.password, -1)
        else:
            self.clipboard.set_text(self.entry_password.get_text(), -1)     

        okimage=ui.get_scaled_image("2714-green.svg")
        self.button_password_copy.set_image(okimage)

    def on_password_show(self,widget):
        if self.password_id:
            pc=PasswordController()
            db_password=pc.get(self.password_id)
            self.entry_password.set_text(db_password.password)           
