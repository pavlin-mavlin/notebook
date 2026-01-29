from models.node import Node,NodeType 
from peewee import fn

class NodeController(object):

    def __init__(self):
        '''
        Constructor
        '''
    
    def create_table(self):
        Node.create_table() 
    
    def create_root(self):
        hasroot=Node.select().where(Node.parent_id >> None).exists()
        if not hasroot:
            Node.create(name="Root",expanded=True,type=NodeType.FOLDER.value,parent=None)
     
    def save(self,node):
        is_new=node.node_id is None
        node.save(is_new)        
        if is_new:
            node.weight=node.node_id
            node.save()        

    def get(self,node_id):
        node=Node.select().where(Node.node_id==node_id).get()
        return node
    
    def get_root(self):
        root_node=Node.select().where(Node.parent_id >> None).get()
        return root_node
        
    def list(self):
        return  Node.select()
        
    def delete(self,node_id):
        Node.delete_by_id(node_id)
            
    def save_expanded(self,node_id):
        node=self.get(node_id)
        node.expanded=True
        node.save()
            
    def save_collapsed(self,node_id):
        node=self.get(node_id)
        node.expanded=False
        node.save()         
        
    def select_by_parent(self,query,parent_id):
        results=query.where(Node.parent_id==parent_id).order_by(Node.weight)
        return results
    
    def swap_weights(self,node_id1,node_id2):
        node1=self.get(node_id1)
        node2=self.get(node_id2)
        weight1=node1.weight
        weight2=node2.weight
        node1.weight=weight2
        node2.weight=weight1
        node1.save()
        node2.save()
    
    def change_parent(self,node_id,new_parent_id):
        max_weight=Node.select(fn.Max(Node.weight)).where(Node.parent_id==new_parent_id).scalar()
        if not max_weight:
            max_weight=0
        
        node=self.get(node_id)
        node.parent=new_parent_id
        node.weight=max_weight+1
        node.save()
        
       
