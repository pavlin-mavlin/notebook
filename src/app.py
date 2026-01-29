import gi
import sys
from ui.appwindow import AppWindow

from models.basemodel import database
from controllers.nodecontroller import NodeController
from controllers.urlcontroller import UrlController
from controllers.memocontroller import MemoController
from controllers.passwordcontroller import PasswordController
from controllers.settingcontroller import SettingController
from controllers.commandcontroller import CommandController
from ui.commandsdialog import CommandsDialog
import ui

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio,Gtk

# вроде даже есть визуальный дизайнер https://stackoverflow.com/questions/14878665/python-gtk-development-in-linux-using-eclipse-pydev-unresolved-import-gtk#21482193
class App(Gtk.Application):

    
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, application_id="com.learnpython.notebook",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        GLib.set_application_name("notebook")
        self.db_name='notebook.db'
        
        self.add_main_option("database", ord("d"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.STRING, "database", None)
                

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()        
        options = options.end().unpack()

        if "database" in options:
            self.db_name=options["database"]
            
        self.activate()
        return 0

    def do_activate(self):
        database.init(self.db_name)
        
        nc=NodeController()
        nc.create_table()
        nc.create_root()
        #create other tables here by calling their controller
        UrlController().create_table()
        MemoController().create_table()
        PasswordController().create_table()
        SettingController().create_table()
        CommandController().create_table()
        
        if not ui.app_window:
            ui.app_window = AppWindow(application=self, title="Notebook")

        ui.app_window.present()
        
    def do_startup(self):
        Gtk.Application.do_startup(self)
        #action = Gio.SimpleAction.new("settings", None)
        #action.connect("activate", self.on_settings)
        #self.add_action(action)

        action = Gio.SimpleAction.new("commands", None)
        action.connect("activate", self.on_commands)
        self.add_action(action)        
        
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        #как это сделать в xml?
        builder = Gtk.Builder.new_from_file("src/ui/menu.xml")
        main_menu=builder.get_object("main-menu")
        file_menu=builder.get_object("file-menu")
        main_menu.append_submenu("Файл",file_menu)
        self.set_menubar(main_menu)


    def on_quit(self, action, param):
        if ui.app_window: 
            ui.app_window.destroy() #без этого appwindow.on_paned_unrealize не выполняется
            
        self.quit()        
        
    #def on_settings(self,action, param):
        #dialog = SettingsDialog(self.window)
        #response = dialog.run()
        #if response == Gtk.ResponseType.OK:
            #sc=SettingController()
            #sc.update("open_command", setting_value)
        
        #dialog.destroy()

    def on_commands(self,action, param):
        dialog = CommandsDialog(ui.app_window)
        dialog.run()        
        dialog.destroy()        
        

if __name__ == "__main__":
    app = App()
    app.run(sys.argv)

    
