import gi
from controllers.commandcontroller import CommandController
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,Gdk
from ui.editorinterface import EditorInterface
import ui
from controllers.urlcontroller import UrlController
from models.url import Url 
import subprocess

class EditorUrl(EditorInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.set_orientation(Gtk.Orientation.VERTICAL)
        
        grid = Gtk.Grid(border_width=10,row_spacing=10,column_spacing=10)
        
        label_url = Gtk.Label(label="URL ссылка: ",xalign=1)
        grid.add(label_url)
        
        self.button_url_copy=Gtk.Button.new_from_icon_name("edit-copy",Gtk.IconSize.BUTTON)
        self.button_url_copy.connect("clicked",self.on_button_url_copy)
        grid.attach(self.button_url_copy,1,0,1,1)            
        
        hBox=Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)     
        
        self.entry_url = Gtk.Entry(hexpand=True)
        self.entry_url.set_max_length(255)    
        hBox.pack_start(self.entry_url,True,True,0)
        
        command_store = Gtk.ListStore(str, str)
        cc=CommandController()
        commands=cc.list()
        for command in commands:
            command_store.append([str(command.command_id),command.name])
        
        self.combo_command = Gtk.ComboBox.new_with_model(command_store)
        self.combo_command.set_id_column(0)
        renderer_text = Gtk.CellRendererText()
        self.combo_command.pack_start(renderer_text, True)
        self.combo_command.add_attribute(renderer_text, "text", 1)
        hBox.pack_end(self.combo_command,False,False,0)
        
        default_command=cc.get_default()
        if default_command:
            self.combo_command.set_active_id(str(default_command.command_id))
        
        grid.attach_next_to(hBox,self.button_url_copy,Gtk.PositionType.RIGHT,1,1)

        open_image=ui.get_scaled_image("25b6.svg")
        button_url_open=Gtk.Button(image=open_image)
        button_url_open.connect("clicked",self.on_url_open)
        grid.attach_next_to(button_url_open,hBox,Gtk.PositionType.RIGHT,1,1)
        
        label_username = Gtk.Label(label="Имя пользователя: ",xalign=1)
        grid.attach(label_username,0,1,1,1)
        
        self.button_username_copy=Gtk.Button.new_from_icon_name("edit-copy",Gtk.IconSize.BUTTON)
        self.button_username_copy.connect("clicked",self.on_username_copy)
        grid.attach(self.button_username_copy,1,1,1,1)
        
        self.entry_username = Gtk.Entry(hexpand=True)
        self.entry_username.set_max_length(255)    
        grid.attach_next_to(self.entry_username,self.button_username_copy,Gtk.PositionType.RIGHT,1,1)
        
        label_password=Gtk.Label(label="Пароль: ",xalign=1)
        grid.attach(label_password,0,2,1,1)
        
        self.button_password_copy=Gtk.Button.new_from_icon_name("edit-copy",Gtk.IconSize.BUTTON)
        self.button_password_copy.connect("clicked",self.on_password_copy)
        grid.attach(self.button_password_copy,1,2,1,1)
        
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
        self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)
        self.add(scrolledwindow)
        
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        
        self.show_all()

    def load_data(self, node_id: int):
        self.url_id=None    
        if node_id!=-1:
            uc=UrlController()
            db_url=uc.get_by_node_id(node_id)
            self.node_id=node_id
            
            if db_url:
                self.entry_url.set_text(db_url.url)
                if db_url.command_id:
                    self.combo_command.set_active_id(str(db_url.command_id))
                    
                self.entry_username.set_text(db_url.username)
                self.entry_password.set_text(ui.make_password_placeholder(db_url.password))
                textbuffer = self.textview.get_buffer()
                textbuffer.set_text(db_url.description)
                self.url_id=db_url.url_id
    
    def save_data(self):
        uc=UrlController()
         
        if self.url_id:
            db_url=uc.get(self.url_id)
        else:
            db_url=Url()
            db_url.node_id=self.node_id
        
        db_url.url=self.entry_url.get_text()
        command_id=self.combo_command.get_active_id()
        if command_id:
            db_url.command_id=int(command_id)        
        
        db_url.username=self.entry_username.get_text()
        
        if "•" not in self.entry_password.get_text():
            db_url.password=self.entry_password.get_text()
            
        textbuffer = self.textview.get_buffer()
        db_url.description=textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(),True)
        uc.update(db_url)
        self.url_id=db_url.url_id        
            
    def on_url_open(self,widget):
        command_id=self.combo_command.get_active_id()        
        url=self.entry_url.get_text()
                         
        if command_id and url:
            cc=CommandController()
            command=cc.get(int(command_id))
            if command.command:
                subprocess.Popen([command.command, url])
            else:
                urlparts=url.split()
                subprocess.Popen(urlparts)
        else:
            dialog = Gtk.MessageDialog(
                transient_for=ui.app_window,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Нет команды или ссылки",
                )

            dialog.run()
            dialog.destroy()
            
    def on_username_copy(self, widget):
        self.clipboard.set_text(self.entry_username.get_text(), -1)
        okimage=ui.get_scaled_image("2714-green.svg")
        self.button_username_copy.set_image(okimage)
        
    def on_password_copy(self, widget):
        if "•" in self.entry_password.get_text():
            uc=UrlController()
            db_url=uc.get(self.url_id)
            self.clipboard.set_text(db_url.password, -1)
        else:
            self.clipboard.set_text(self.entry_password.get_text(), -1)     

        okimage=ui.get_scaled_image("2714-green.svg")
        self.button_password_copy.set_image(okimage)

    def on_password_show(self,widget):
        if self.password_id:
            uc=UrlController()
            db_url=uc.get(self.url_id)
            self.entry_password.set_text(db_url.password)           

    def on_button_url_copy(self,widget):
        self.clipboard.set_text(self.entry_url.get_text(), -1)
        okimage=ui.get_scaled_image("2714-green.svg")
        widget.set_image(okimage)
        