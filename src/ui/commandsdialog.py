import gi
from controllers.commandcontroller import CommandController
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ui.commandeditdialog import CommandEditDialog
from models.command import Command

class CommandsDialog(Gtk.Dialog):

    def __init__(self, parent):
        super().__init__(title="Список профилей", transient_for=parent, flags=0)
        
        self.set_default_size(300, 150)
        content_box = self.get_content_area()
        self.add_buttons("_OK", Gtk.ResponseType.OK)
        
        hBox=Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)                
        
        self.listbox = Gtk.ListBox()
        self.populate_list()
        
        hBox.pack_start(self.listbox,True,True,0)
        
        buttons_box=Gtk.Box(spacing=10,orientation=Gtk.Orientation.VERTICAL)
        
        button_add=Gtk.Button(label="Добавить")
        button_add.connect("clicked",self.on_button_add)
        buttons_box.add(button_add)
        
        button_edit=Gtk.Button(label="Правка")
        button_edit.connect("clicked",self.on_button_edit)
        buttons_box.add(button_edit)
        
        button_delete=Gtk.Button(label="Удалить")
        button_delete.connect("clicked",self.on_button_delete)
        buttons_box.add(button_delete)
                        
        hBox.pack_end(buttons_box,False,False,0)
        
        content_box.add(hBox)
        
        self.show_all()
        
    def on_button_add(self, widget):
        dialog = CommandEditDialog(self)
        response=dialog.run()
        if response == Gtk.ResponseType.OK:
            command=Command()
            command.name=dialog.entry_name.get_text()
            command.command=dialog.entry_command.get_text()
            command.default=dialog.check_default.get_active()
            cc=CommandController()
            cc.update(command)
            self.populate_list()
                            
        dialog.destroy() 
        
    def on_button_edit(self,widget):
        row=self.listbox.get_selected_row()
        if row:
            dialog = CommandEditDialog(self,row.command_id)
            response=dialog.run()
            if response == Gtk.ResponseType.OK:
                cc=CommandController()
                command=cc.get(row.command_id)
                command.name=dialog.entry_name.get_text()
                command.command=dialog.entry_command.get_text()
                command.default=dialog.check_default.get_active()
                cc.update(command)
                self.populate_list()
                                
            dialog.destroy() 
            
    def on_button_delete(self,widget):
        row=self.listbox.get_selected_row()
        if row:
            cc=CommandController()
            can_delete=cc.can_delete(row.command_id)
            if can_delete:
                dialog = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.QUESTION,
                    buttons=Gtk.ButtonsType.YES_NO,
                    text="Вы уверены, что хотите удалить этот элемент?",)
                
                response = dialog.run()            
            
                if response == Gtk.ResponseType.YES:     
                    cc.delete(row.command_id)
                    self.populate_list()
                
                dialog.destroy()
            else:
                dialog = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.QUESTION,
                    buttons=Gtk.ButtonsType.OK,
                    text="Нельзя удалять эту команду",)
                
                dialog.run()              
                dialog.destroy()
            
    def populate_list(self):
        children=self.listbox.get_children()
        for child in children:
            self.listbox.remove(child)
        
        cc=CommandController()
        commands=cc.list()
        for command in commands:
            self.listbox.add(ListBoxRowWithData(command.name,command.command_id))  
        
        self.listbox.show_all()      
        
class ListBoxRowWithData(Gtk.ListBoxRow):

    def __init__(self, name,command_id):
        super().__init__()
        self.command_id = command_id
        self.add(Gtk.Label(label=name, xalign=0))
                