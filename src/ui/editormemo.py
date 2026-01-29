import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ui.editorinterface import EditorInterface
from controllers.memocontroller import MemoController
from models.memo import Memo

class EditorMemo(EditorInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        scrolledwindow = Gtk.ScrolledWindow(border_width=10)
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)
        self.add(scrolledwindow)
        self.memo_id=None  
        self.show_all()

    def load_data(self, node_id: int):
        self.memo_id=None    
        if node_id!=-1:
            mc=MemoController()
            db_memo=mc.get_by_node_id(node_id)
            self.node_id=node_id
            
            if db_memo:
                textbuffer = self.textview.get_buffer()
                textbuffer.set_text(db_memo.memo)
                self.memo_id=db_memo.memo_id
    
    def save_data(self):
        mc=MemoController()
         
        if self.memo_id:
            db_memo=mc.get(self.memo_id)
        else:
            db_memo=Memo()
            db_memo.node_id=self.node_id
        
        textbuffer = self.textview.get_buffer()
        db_memo.memo=textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(),True)
        mc.update(db_memo)
        self.memo_id=db_memo.memo_id
                