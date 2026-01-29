import gi
from controllers.nodecontroller import NodeController

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

app_window=None

def get_scaled_image(path):
    pb=get_scaled_pixbuf(path)
    image=Gtk.Image.new_from_pixbuf(pb)        
    return image

def get_scaled_pixbuf(path):
    pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename="images/"+path, 
        width=-1, height=20, preserve_aspect_ratio=True)
    
    return pb   

def make_password_placeholder(password):
    placeholder=""
    if password:
        for x in range(1, len(password)):
            placeholder=placeholder+"•"
            
    return placeholder
