import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class SettingsDialog(Gtk.Dialog):

    def __init__(self, parent):
        super().__init__(title="Настройки", transient_for=parent, flags=0)

        self.add_buttons(
            "Отмена", Gtk.ResponseType.CANCEL, "_OK", Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)
        box = self.get_content_area()
        
        grid = Gtk.Grid(border_width=10,row_spacing=10,column_spacing=10)
        #label_open_command = Gtk.Label(label="Команда на открытие URL:")
        #grid.add(label_open_command)
        
        #self.entry_open_command = Gtk.Entry(hexpand=True)
        #self.entry_open_command.set_max_length(255)     
        #grid.attach_next_to(self.entry_open_command,label_open_command,Gtk.PositionType.RIGHT,1,1)
        
        #sc=SettingController()
        #setting=sc.get("open_command")
        
        #if setting:
            #self.entry_open_command.set_text(setting.svalue)
                        
        box.add(grid)

        self.show_all()
        