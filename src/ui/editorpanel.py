import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from models.node import NodeType
from ui.editorinterface import EditorInterface
from ui.editorurl import EditorUrl
import ui
from ui.editormemo import EditorMemo
from ui.editorpassword import EditorPassword

class EditorPanel(Gtk.Box):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        toolbar=Gtk.Toolbar()
        toolbar.set_border_width(5)
        
        self.editor=None
        # здесь примеры стандартных иконок https://www.tutorialspoint.com/pygtk/pygtk_toolbar_class.htm
        image_save=ui.get_scaled_image("1f4be.svg")
        self.button_save=Gtk.ToolButton(icon_widget=image_save,sensitive=False) #stock_id=Gtk.STOCK_NEW  
        self.button_save.connect("clicked",self.on_button_save_clicked)     
        toolbar.add(self.button_save)
                
        image_revert=ui.get_scaled_image("revert.svg")
        self.button_revert=Gtk.ToolButton(icon_widget=image_revert,sensitive=False)
        self.button_revert.connect("clicked",self.on_button_revert_clicked)
        toolbar.add(self.button_revert)
        
        self.node_id=None
        self.node_type=None
        
        self.add(toolbar)
           
    def on_node_changed(self,node_id: int,node_type: int):        
        if self.editor:
            self.editor.save_data()
            self.remove(self.editor)
            self.editor.destroy()
            self.editor=None
            self.button_save.set_sensitive(False)
            self.button_revert.set_sensitive(False)        

        self.node_id=node_id
        self.node_type=node_type

        if self.node_id and self.node_id!=-1:      
            self.editor=self.get_editor(self.node_type)    
            if self.editor:            
                self.add(self.editor)
                self.button_save.set_sensitive(True)
                self.button_revert.set_sensitive(True)                
                self.editor.load_data(self.node_id)             
                        
    def on_node_edited(self,node_id: int,node_type: int):        
        if self.editor:
            self.on_button_save_clicked(self)
            
        self.node_id=node_id
        self.node_type=node_type
        
        if not self.editor:
            self.editor=self.get_editor(self.node_type)    
            if self.editor:            
                self.add(self.editor)
                self.button_save.set_sensitive(True)
                self.button_revert.set_sensitive(True)
                self.editor.load_data(self.node_id)
                
    #фабрика
    def get_editor(self,ed_type: NodeType)->EditorInterface:
        editor=None
        if ed_type==NodeType.URL.value:
            editor=EditorUrl()
        
        if ed_type==NodeType.MEMO.value:
            editor=EditorMemo()
            
        if ed_type==NodeType.PASSWORD.value:
            editor=EditorPassword()            
            
        return editor            
    
    def on_button_save_clicked(self,widget):
        if self.editor and self.node_id:
            self.editor.save_data()
            
    def on_button_revert_clicked(self,widget):
        if self.editor and self.node_id:
            dialog = Gtk.MessageDialog(
                transient_for=ui.app_window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Вы уверены, что хотите отменить изменения?",
                )

            response = dialog.run()
            dialog.destroy()
            
            if response == Gtk.ResponseType.YES:
                self.editor.load_data(self.node_id)
            