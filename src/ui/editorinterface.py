import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class EditorInterface(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def load_data(self, node_id: int):
        pass
    
    def save_data(self):
        pass    
