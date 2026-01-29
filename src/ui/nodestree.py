import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from models.node import Node,NodeType
import ui
from controllers.nodecontroller import NodeController

class NodesTree(Gtk.Box):        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        toolbar=Gtk.Toolbar()
        toolbar.set_border_width(5)
                
        # здесь примеры стандартных иконок https://www.tutorialspoint.com/pygtk/pygtk_toolbar_class.htm
        
        image_folder=ui.get_scaled_image("folder-add.svg")
        self.button_folder=Gtk.ToolButton(icon_widget=image_folder,sensitive=False)  
        self.button_folder.connect("clicked",self.on_button_folder_clicked)     
        toolbar.add(self.button_folder)
        
        image_memo=ui.get_scaled_image("memo-add.svg")
        self.button_memo=Gtk.ToolButton(icon_widget=image_memo,sensitive=False)
        self.button_memo.connect("clicked",self.on_button_memo_clicked)
        toolbar.add(self.button_memo)
        
        image_password=ui.get_scaled_image("password-add.svg")
        self.button_password=Gtk.ToolButton(icon_widget=image_password,sensitive=False)
        self.button_password.connect("clicked",self.on_button_password_clicked)
        toolbar.add(self.button_password)
                
        image_url=ui.get_scaled_image("link-add.svg")
        self.button_url=Gtk.ToolButton(icon_widget=image_url,sensitive=False)
        self.button_url.connect("clicked",self.on_button_url_clicked)
        toolbar.add(self.button_url)

        image_delete=ui.get_scaled_image("274c.svg")
        self.button_delete=Gtk.ToolButton(icon_widget=image_delete,sensitive=False)
        self.button_delete.connect("clicked",self.on_button_delete_clicked)
        toolbar.add(self.button_delete)
        
        image_up=ui.get_scaled_image("2b06.svg")
        self.button_up=Gtk.ToolButton(icon_widget=image_up,sensitive=False)
        self.button_up.connect("clicked",self.on_button_up_clicked)
        toolbar.add(self.button_up)
        
        image_down=ui.get_scaled_image("2b07.svg")
        self.button_down=Gtk.ToolButton(icon_widget=image_down,sensitive=False)
        self.button_down.connect("clicked",self.on_button_down_clicked)
        toolbar.add(self.button_down)
        
        image_cut=ui.get_scaled_image("2702-rot.svg")
        self.button_cut=Gtk.ToolButton(icon_widget=image_cut,sensitive=False)
        self.button_cut.connect("clicked",self.on_button_cut_clicked)
        toolbar.add(self.button_cut)
        
        image_paste=ui.get_scaled_image("1f4cb.svg")
        self.button_paste=Gtk.ToolButton(icon_widget=image_paste,sensitive=False)
        self.button_paste.connect("clicked",self.on_button_paste_clicked)
        toolbar.add(self.button_paste)
        
        self.cut_path=None
        
        self.set_homogeneous(False)
        self.pack_start(toolbar,False,False,0)
                        
        self.folder_pixbuf=ui.get_scaled_pixbuf("1f4c1.svg")
        self.memo_pixbuf=ui.get_scaled_pixbuf("1f4dd.svg")
        self.password_pixbuf=ui.get_scaled_pixbuf("1f511.svg")
        self.url_pixbuf=ui.get_scaled_pixbuf("1f517.svg")
                
        store = Gtk.TreeStore(str,int,GdkPixbuf.Pixbuf,int,int)            
        
        expanded_paths=[]
        self.populate_tree(store,expanded_paths)        
        
        self.tree = Gtk.TreeView(model=store,enable_tree_lines=True)
        self.tree.set_headers_visible(False)
        
        self.column = Gtk.TreeViewColumn("Structure")
        
        self.col_cell_text = Gtk.CellRendererText()
        self.col_cell_text.set_property("editable", True)
        self.col_cell_text.connect("edited",self.on_tree_edited)
        col_cell_img = Gtk.CellRendererPixbuf()
        self.column.pack_start(col_cell_img, False)
        self.column.pack_start(self.col_cell_text, True)
        self.column.add_attribute(self.col_cell_text, "text", 0)
        self.column.add_attribute(col_cell_img, "pixbuf", 2)
        
        self.tree.append_column(self.column)
        self.tree.expand_row(Gtk.TreePath.new_first(),False)
        select = self.tree.get_selection()
        select.connect("changed", self.on_tree_selection_changed)
        self.tree.connect("row_expanded",self.on_tree_row_expanded)
        self.tree.connect("row_collapsed",self.on_tree_row_collapsed)
        
        for path in expanded_paths:
            self.tree.expand_row(path,False)
        
        #пример реакции на двойное нажатие
        #https://github.com/mtwebster/git-monkey/blob/master/usr/lib/git-monkey/git-monkey.py       
        sw=Gtk.ScrolledWindow()
        sw.add(self.tree)
        self.pack_end(sw,True,True,0)    
    
    # рекурсивная функция для наполнения дерева с учётом веса узлов
    def populate_tree_branch(self,nc: NodeController,db_nodes,parent_id,pixbufs,expanded_paths,store,parent_tree_node):
        children=nc.select_by_parent(db_nodes, parent_id)
        
        for db_node in children:
            tree_node=store.append(parent_tree_node, [db_node.name,db_node.type,pixbufs[db_node.type],
                                                      db_node.parent_id,db_node.node_id]) 
            if db_node.expanded:
                expanded_paths.append(store.get_path(tree_node))
            
            self.populate_tree_branch(nc, db_nodes, db_node.node_id, pixbufs, expanded_paths, store, tree_node)
    
    def on_tree_selection_changed(self,selection):
        model, treeiter = selection.get_selected()
        if treeiter is None:
            self.button_delete.set_sensitive(False)
            self.button_folder.set_sensitive(False)
            self.button_memo.set_sensitive(False)
            self.button_password.set_sensitive(False)
            self.button_url.set_sensitive(False)
            self.button_up.set_sensitive(False)
            self.button_down.set_sensitive(False)
            self.button_cut.set_sensitive(False)
            self.button_paste.set_sensitive(False)
            self.subscriber.on_node_changed(self.subscriber,None) 
        else:
            node_type=model[treeiter][1]
            node_id=model[treeiter][4]
            
            self.button_folder.set_sensitive(True)
            self.button_memo.set_sensitive(True)
            self.button_password.set_sensitive(True)
            self.button_url.set_sensitive(True)
            self.button_cut.set_sensitive(True)
            self.button_paste.set_sensitive(False)
            
            if node_type==NodeType.FOLDER.value:
                self.button_paste.set_sensitive(self.cut_path is not None)
                self.button_delete.set_sensitive(False)
                #если папка не root и пустая - можно удалять
                if not model[treeiter][3]==0 and not model.iter_has_child(treeiter):
                    self.button_delete.set_sensitive(True)                    
                
            if node_type==NodeType.MEMO.value:
                self.button_delete.set_sensitive(True) 
                                 
            if node_type==NodeType.PASSWORD.value:
                self.button_delete.set_sensitive(True)

            if node_type==NodeType.URL.value:
                self.button_delete.set_sensitive(True)
            
            self.button_up.set_sensitive(model.iter_previous(treeiter) is not None)
            self.button_down.set_sensitive(model.iter_next(treeiter) is not None)
            
            self.subscriber.on_node_changed(node_id=node_id,node_type=node_type)     
            
    
    def on_button_folder_clicked(self, widget):
        tree_item=["Папка",NodeType.FOLDER.value,self.folder_pixbuf,-1,-1]
        self.create_node(tree_item)        
            
    def on_button_memo_clicked(self, widget):
        tree_item=["Заметка",NodeType.MEMO.value,self.memo_pixbuf,-1,-1]
        self.create_node(tree_item)  

    def on_button_password_clicked(self, widget):
        tree_item=["Пароль",NodeType.PASSWORD.value,self.password_pixbuf,-1,-1]
        self.create_node(tree_item)  
            
    def on_button_url_clicked(self, widget):    
        tree_item=["Ссылка",NodeType.URL.value,self.url_pixbuf,-1,-1]
        self.create_node(tree_item)      
            
    def on_button_delete_clicked(self, widget):
        dialog = Gtk.MessageDialog(
            flags=0,
            transient_for=ui.app_window,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Вы уверены, что хотите удалить этот элемент?",
        )

        response = dialog.run()
        dialog.destroy()
        
        if response == Gtk.ResponseType.YES:
            selection=self.tree.get_selection()
            if selection:
                model, treeiter = selection.get_selected()
                node_id=model[treeiter][4]
                model.remove(treeiter)
                NodeController().delete(node_id)                
        
    def on_tree_edited(self,cell_renderer, path, new_text):
        treeiter = self.tree.get_model().get_iter(path)
        tree_item=self.tree.get_model()[treeiter]
        tree_item[0]=new_text
        controller=NodeController()
        db_node=None
        if tree_item[4]==-1:            
            db_node=Node(name=new_text,expanded=True,parent_id=tree_item[3],type=tree_item[1])            
        else:
            db_node=controller.get(tree_item[4])
            db_node.name=new_text
            
        controller.save(db_node)
        
        if tree_item[4]==-1:
            tree_item[4]=db_node.node_id
        
        self.subscriber.on_node_edited(node_id=db_node.node_id,node_type=db_node.type)
    
    def create_node(self,tree_item): 
        selection=self.tree.get_selection()
        if selection:
            model, treeiter = selection.get_selected()
            parent_node=model[treeiter]       
            
            if parent_node[1]!=NodeType.FOLDER.value:
                treeiter=model.iter_parent(treeiter)
                parent_node=model[treeiter] 
                
            tree_item[3]=parent_node[4]
            new_iter=model.append(treeiter,tree_item)
            selection.select_iter(new_iter)
            new_path=model.get_path(new_iter)
            self.tree.expand_to_path(new_path)
            self.tree.set_cursor_on_cell(new_path,self.column,self.col_cell_text,True)


    def on_tree_row_collapsed(self,widget,treeiter,path):
        tree_item=self.tree.get_model()[treeiter]
        nc=NodeController()
        nc.save_collapsed(tree_item[4])
        
    def on_tree_row_expanded(self,widget,treeiter,path):
        tree_item=self.tree.get_model()[treeiter]
        nc=NodeController()
        nc.save_expanded(tree_item[4])       

    def on_button_up_clicked(self,widget):
        selection=self.tree.get_selection()
        if selection:
            model, treeiter = selection.get_selected()
            prev_iter=model.iter_previous(treeiter)
            if prev_iter:
                nc=NodeController()
                nc.swap_weights(model[treeiter][4], model[prev_iter][4])
                model.swap(treeiter,prev_iter)            
    
    def on_button_down_clicked(self,widget):
        selection=self.tree.get_selection()
        if selection:
            model, treeiter = selection.get_selected()
            next_iter=model.iter_next(treeiter)
            if next_iter:
                nc=NodeController()
                nc.swap_weights(model[treeiter][4], model[next_iter][4])
                model.swap(treeiter,next_iter)
    
    def on_button_cut_clicked(self,widget):
        selection=self.tree.get_selection()
        if selection:
            model, treeiter = selection.get_selected()
            self.cut_path=model.get_path(treeiter)
    
    def on_button_paste_clicked(self,widget):
        if self.cut_path:
            selection=self.tree.get_selection()
            if selection:
                model, treeiter = selection.get_selected()
                #FIXME: не разрешать вставлять в качестве дочерней ноды самого себя
                
                #TreeModel не позволяет менять родителя у ноды, поэтому вносим изменения в БД, а затем перезаливаем
                #через путь self.cut_path получить ноду по этому пути, извлечь node_id
                source_iter=model.get_iter(self.cut_path)
                source_node=model[source_iter]
                
                # новая папка
                dest_node=model[treeiter]
            
                nc=NodeController()
                nc.change_parent(source_node[4], dest_node[4])
                
                model.clear()
                
                expanded_paths=[]
                self.populate_tree(model,expanded_paths)
                
                self.tree.expand_row(Gtk.TreePath.new_first(),False)
                
                for path in expanded_paths:
                    self.tree.expand_row(path,False)
                          
                self.cut_path=None
                
    def populate_tree(self,model,expanded_paths):
        pixbufs={
            1: self.folder_pixbuf,
            2: self.memo_pixbuf,
            3: self.password_pixbuf,
            4: self.url_pixbuf
            }
        
        nc=NodeController()
        db_root=nc.get_root()
        root_node=model.append(None, ["Root",NodeType.FOLDER.value,self.folder_pixbuf,0,db_root.node_id])   
        db_nodes=nc.list()                        
        self.populate_tree_branch(nc, db_nodes, db_root.node_id, pixbufs, expanded_paths, model, root_node)  
        
            
