import gi
from controllers.commandcontroller import CommandController

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class CommandEditDialog(Gtk.Dialog):


    def __init__(self, parent,command_id=None):
        super().__init__(title="Команда", transient_for=parent, flags=0)
        
        self.add_buttons("Отмена", Gtk.ResponseType.CANCEL, "_OK", Gtk.ResponseType.OK)
        
        self.set_default_size(300, 100)
        box = self.get_content_area()
        
        grid = Gtk.Grid(border_width=10,row_spacing=10,column_spacing=10)
        
        label_name = Gtk.Label(label="Название: ",xalign=1)
        grid.add(label_name)
        
        self.entry_name = Gtk.Entry(hexpand=True)
        self.entry_name.set_max_length(255)    
        grid.attach_next_to(self.entry_name,label_name,Gtk.PositionType.RIGHT,1,1)
        
        label_command=Gtk.Label(label="Команда: ",xalign=1)
        grid.attach(label_command,0,1,1,1)
        
        self.entry_command = Gtk.Entry(hexpand=True)
        self.entry_command.set_max_length(255)   
        grid.attach_next_to(self.entry_command,label_command,Gtk.PositionType.RIGHT,1,1)                
        
        self.check_default=Gtk.CheckButton.new_with_label("По умолчанию")
        grid.attach(self.check_default,1,2,1,1)
        
        box.add(grid)
        self.show_all()
        
        if command_id:
            cc=CommandController()
            command=cc.get(command_id)
            self.entry_name.set_text(command.name)
            self.entry_command.set_text(command.command)
            self.check_default.set_active(command.default)
            