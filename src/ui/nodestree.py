import tkinter as tk
from tkinter import ttk
from models.node import Node,NodeType
import ui
from controllers.nodecontroller import NodeController
from ui.entrypopup import EntryPopup

class NodesTree(tk.Frame):        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.cut_item_id=None        
        
        toolbar = tk.Frame(self, borderwidth = 1, relief=tk.RAISED)    
            
        self.image_folder_add = tk.PhotoImage(file="images/folder-add.png") # self нужно, хотя не используется        
        self.button_folder = tk.Button(toolbar, image=self.image_folder_add, state=tk.DISABLED,width=34,command=self.on_folder_add) #relief=tk.FLAT, 
        self.button_folder.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.image_memo_add=tk.PhotoImage(file="images/memo-add.png")
        self.button_memo=tk.Button(toolbar, image=self.image_memo_add, state=tk.DISABLED,width=34,command=self.on_memo_add)
        self.button_memo.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.image_password_add=tk.PhotoImage(file="images/password-add.png")
        self.button_password=tk.Button(toolbar, image=self.image_password_add, state=tk.DISABLED,width=34,command=self.on_password_add)
        self.button_password.pack(side=tk.LEFT, padx=2, pady=5)
                
        self.image_url_add=tk.PhotoImage(file="images/link-add.png")
        self.button_url=tk.Button(toolbar, image=self.image_url_add,  state=tk.DISABLED,width=34,command=self.on_url_add)
        self.button_url.pack(side=tk.LEFT, padx=2, pady=5)

        self.image_delete=tk.PhotoImage(file="images/274c.png")
        self.button_delete=tk.Button(toolbar, image=self.image_delete,  state=tk.DISABLED,width=34,command=self.on_delete)
        self.button_delete.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.image_up=tk.PhotoImage(file="images/2b06.png")
        self.button_up=tk.Button(toolbar, image=self.image_up,  state=tk.DISABLED,width=34,command=self.on_item_up)
        self.button_up.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.image_down=tk.PhotoImage(file="images/2b07.png")
        self.button_down=tk.Button(toolbar, image=self.image_down,  state=tk.DISABLED,width=34,command=self.on_item_down)
        self.button_down.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.image_cut=tk.PhotoImage(file="images/2702-rot.png")
        self.button_cut=tk.Button(toolbar, image=self.image_cut, width=34, state=tk.DISABLED,command=self.on_cut)
        self.button_cut.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.image_paste=tk.PhotoImage(file="images/1f4cb.png")
        self.button_paste=tk.Button(toolbar, image=self.image_paste, width=34, state=tk.DISABLED,command=self.on_paste)
        self.button_paste.pack(side=tk.LEFT, padx=2, pady=5)
                
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        #self.image_folder=tk.PhotoImage(file="images/1f4c1.png")
        #self.image_memo=tk.PhotoImage(file="images/1f4dd.png")
        #self.image_password=tk.PhotoImage(file="images/1f511.png")
        #self.image_url=tk.PhotoImage(file="images/1f517.png")        
        
        self.node_images={
            NodeType.FOLDER.value: tk.PhotoImage(file="images/1f4c1.png"),
            NodeType.MEMO.value: tk.PhotoImage(file="images/1f4dd.png"),
            NodeType.PASSWORD.value: tk.PhotoImage(file="images/1f511.png"),
            NodeType.URL.value: tk.PhotoImage(file="images/1f517.png") 
            }
        
        self.tree_frame = ttk.Frame(self)        
        self.tree=ttk.Treeview(self.tree_frame,show="tree")
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        #https://stackoverflow.com/questions/18562123/how-to-make-ttk-treeviews-rows-editable     
        self.tree.bind("<Double-1>", lambda event: self.onDoubleClick(event))   
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.populate_tree()

    def populate_tree(self):
        
        nc=NodeController()
        db_root=nc.get_root()
        root_item=self.tree.insert("",tk.END,db_root.node_id,image=self.node_images[NodeType.FOLDER.value],text="Root", open=True,values={db_root.type})
        #db_nodes=nc.list()                        
        #self.populate_tree_branch(nc, db_nodes, db_root.node_id, pixbufs, expanded_paths, model, root_node)  

    def onDoubleClick(self, event):    
        try:  # in case there was no previous popup
            self.entryPopup.destroy()
        except AttributeError:
            pass
    
        # what row and column was clicked on
        rowid = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
    
        self.showPopup(rowid, column)
        
    def showPopup(self,rowid,column):
        # get column position info
        x,y,width,height = self.tree.bbox(rowid, column)
    
        # y-axis offset
        pady = height // 2
    
        # place Entry popup properly         
        text = self.tree.item(rowid, 'text')
        self.entryPopup = EntryPopup(self.tree, rowid, text)
        self.entryPopup.place( x=0, y=y+pady, anchor=tk.W, relwidth=1)
        self.entryPopup.bind("<Destroy>",self.on_entry_destroyed)
        #подписаться на что-то вроде on destroy для сохранения изменений в БД
        
    def item_selected(self,event):
    # Get the selected item ID(s)
        selected_items = self.tree.selection()
    
        if selected_items:
            item_id = selected_items[0]
            item_data = self.tree.item(item_id)            

            self.button_folder.config(state=tk.NORMAL)
            self.button_memo.config(state=tk.NORMAL)
            self.button_password.config(state=tk.NORMAL)
            self.button_url.config(state=tk.NORMAL)
            self.button_cut.config(state=tk.NORMAL)
            self.button_paste.config(state=tk.DISABLED)
            
            node_type=item_data['values'][0]
            
            if node_type==NodeType.FOLDER.value:
                parent_iid=self.tree.parent(item_id)
                self.button_cut.config(state=tk.DISABLED if parent_iid=="" else tk.NORMAL)
                self.button_paste.config(state=tk.NORMAL if self.cut_item_id is not None else tk.DISABLED)                
                self.button_delete.config(state=tk.DISABLED)
                #если папка не root и пустая - можно удалять
                children=self.tree.get_children(item_id)                            
                if not parent_iid=="" and not children:
                    self.button_delete.config(state=tk.NORMAL)                  
                
            if node_type==NodeType.MEMO.value:
                self.button_delete.config(state=tk.NORMAL)
                                 
            if node_type==NodeType.PASSWORD.value:
                self.button_delete.config(state=tk.NORMAL)

            if node_type==NodeType.URL.value:
                self.button_delete.config(state=tk.NORMAL)
            
            next_iid=self.tree.next(item_id)
            prev_iid=self.tree.prev(item_id)
            self.button_up.config(state=tk.DISABLED if prev_iid=="" else tk.NORMAL)
            self.button_down.config(state=tk.DISABLED if next_iid=="" else tk.NORMAL)
            
            #self.subscriber.on_node_changed(node_id=node_id,node_type=node_type)                 
        else:
            self.button_delete.config(state=tk.DISABLED)
            self.button_folder.config(state=tk.DISABLED)
            self.button_memo.config(state=tk.DISABLED)
            self.button_password.config(state=tk.DISABLED)
            self.button_url.config(state=tk.DISABLED)
            self.button_up.config(state=tk.DISABLED)
            self.button_down.config(state=tk.DISABLED)
            self.button_cut.config(state=tk.DISABLED)
            self.button_paste.config(state=tk.DISABLED)
            #self.subscriber.on_node_changed(self.subscriber,None) 

    def create_node(self,node_text,node_type : NodeType): 
        selected_items = self.tree.selection()
        if selected_items:
            parent_id = selected_items[0]                
            parent_data=self.tree.item(parent_id)
            parent_type=parent_data['values'][0]
            
            if parent_type!=NodeType.FOLDER.value:
                parent_id=self.tree.parent(parent_id)
                parent_data=self.tree.item(parent_id)
                        
            node_image=self.node_images[node_type.value]
                        
            child_id=self.tree.insert(parent_id,tk.END,-1,image=node_image,text=node_text, open=True,values={node_type.value})
            self.tree.see(child_id)
            
            self.showPopup(child_id, "#0")

    def on_folder_add(self):
        self.create_node("Папка",NodeType.FOLDER)        
            
    def on_memo_add(self):
        self.create_node("Заметка", NodeType.MEMO)  

    def on_password_add(self):
        self.create_node("Пароль",NodeType.PASSWORD)  
            
    def on_url_add(self):    
        self.create_node("Ссылка",NodeType.URL)    
        
    def on_delete(self):
        result = tk.messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот элемент?",icon=tk.messagebox.QUESTION)
        if result==tk.YES:
            selected_items = self.tree.selection()
            if selected_items:
                node_id = selected_items[0]
                self.tree.delete(node_id)
                NodeController().delete(node_id) 

    def on_item_up(self):
        selected_items = self.tree.selection()
        if selected_items:
            node_id = selected_items[0]
            prev_id=self.tree.prev(node_id)
            if prev_id:
                parent_iid=self.tree.parent(node_id)
                prev_index=self.tree.index(prev_id)
                nc=NodeController()
                nc.swap_weights(node_id, prev_id)
                self.tree.move(node_id,parent_iid,prev_index)
                
    def on_item_down(self):
        selected_items = self.tree.selection()
        if selected_items:
            node_id = selected_items[0]
            next_id=self.tree.next(node_id)
            if next_id:
                parent_iid=self.tree.parent(node_id)
                next_index=self.tree.index(next_id)
                nc=NodeController()
                nc.swap_weights(node_id, next_id)
                self.tree.move(node_id,parent_iid,next_index)
                     
    def on_cut(self):
        selected_items = self.tree.selection()
        if selected_items:
            self.cut_item_id = selected_items[0]
    
    def on_paste(self):
        selected_items = self.tree.selection()
        if selected_items and self.cut_item_id:
            parent_id = selected_items[0]            
            self.tree.move(self.cut_item_id,parent_id,tk.END)            
            nc=NodeController()
            nc.change_parent(self.cut_item_id, parent_id)
            self.tree.see(self.cut_item_id)
            self.cut_item_id=None
    
    def on_entry_destroyed(self,event):        
        if self.entryPopup and self.entryPopup.result:
            node_id=None
            
            if self.tree.exists(-1):
                node_id=-1
            else:
                selected_items = self.tree.selection()
                if selected_items:
                    node_id=selected_items[0]
            
            if node_id:
                node_text=self.tree.item(node_id,"text")  
                item_data=self.tree.item(node_id)  
                node_type=item_data['values'][0]
                
                parent_id=self.tree.parent(node_id)
                
                controller=NodeController()
                db_node=None
                if node_id==-1:            
                    db_node=Node(name=node_text,expanded=True,parent_id=parent_id,type=node_type)            
                else:
                    db_node=controller.get(node_id)
                    db_node.name=node_text
                
                controller.save(db_node)
            
                if node_id==-1:
                    self.tree.delete(node_id)
                    node_image=self.node_images[node_type]
                    child_id=self.tree.insert(parent_id,tk.END,db_node.node_id,image=node_image,text=node_text, open=True,values={node_type})
                    self.tree.selection_set(child_id)
                
        
            #self.subscriber.on_node_edited(node_id=db_node.node_id,node_type=db_node.type)