import gi
from controllers.settingcontroller import SettingController

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ui.nodestree import NodesTree 
from ui.editorpanel import EditorPanel
import ui

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maximize()

        pixbuf = ui.get_scaled_pixbuf("1f4d4.svg")
        self.set_default_icon_list([pixbuf]);
        #https://zetcode.com/gui/pygtk/toolbars/
        # как настраивать внешний вид 
        # https://discourse.gnome.org/t/how-can-we-add-custom-css-styles-to-a-gtkwidget/29529/2                                                 
        
        box_left = NodesTree(spacing=10,orientation=Gtk.Orientation.VERTICAL)
        box_right = EditorPanel(spacing=10,orientation=Gtk.Orientation.VERTICAL)     
        box_left.subscriber=box_right
        
        paned=Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        left_frame=Gtk.Frame(shadow_type=Gtk.ShadowType.IN)
        left_frame.add(box_left)
        
        right_frame=Gtk.Frame(shadow_type=Gtk.ShadowType.IN)
        right_frame.add(box_right)
        paned.add1(left_frame)
        paned.add2(right_frame)
        
        paned.connect("unrealize",self.on_paned_unrealize)        
        
        self.add(paned)
        
        self.show_all()
        
        sc=SettingController()
        setting=sc.get("paned_position")
        if setting and setting.svalue:
            paned.set_position(int(setting.svalue))
        else:
            paned.set_position(100)
                
    def on_paned_unrealize(self,widget):
        sc=SettingController()
        pos=widget.get_position()
        sc.update("paned_position", pos)