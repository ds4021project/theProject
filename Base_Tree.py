import pptree
from copy import deepcopy


class TreeNode(object):
    "Node of a Tree"
    def __init__(self, name:str,parent=None):
        self.name = name
        self.parent=parent
        self.children = []

    def __repr__(self):
        return self.name

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False
        
    def parent(self):
        return self.parent        

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def find_subnode(self,name:str):
        found=None
        for i in self.children:
            if i.name==name:
                found=i

        return found


    def depth(self):    # Depth of current node
        if self.is_root():
            return 0
        else:
            return 1 + self.parent.depth()

    def add_child(self, node):
        node.parent=self
        assert isinstance(node, TreeNode)
        self.children.append(node)

    def disp(self):
        pptree.print_tree(self,'children','name')



class Tree:
    """
    Tree implemenation as a collection of TreeNode objects
    """
    def __init__(self):
       self.root=None
       self.nodes=[]

    def insert(self,node,parent):   # Insert a node into tree
        if parent is not None:
            parent.add_child(node)
        else:
            if self.root is None:
                self.root=node
        self.nodes.append(node)

    def search(self,data):  # Search and return index of Node in Tree
        index=-1
        for N in self.nodes:
            index+=1
            if N.name == data:
                break
        if index == len(self.nodes)-1:
            return -1  #node not found
        else:
            return index

    def getNode(self,id):
        return self.nodes[id]

    def root(self):
        return self.root
    
class FileSystem:
    """FileSystem class via tree implementation"""
    def __init__(self):
        self.dir_tree=Tree()
        self.dir_tree.root=TreeNode("this PC",None)
        self.current=self.dir_tree.root
        self.dir_track=[self.dir_tree.root]
        self.go_forward_arrow_stack=[]
        self.virtual_copy_space=None

    def pwd(self):
        str=""
        for i in self.dir_track:
            str+=i.name+"//"
        print(str[:-2])
        return str[-2]


    def create_drive(self,node:TreeNode):
        if self.dir_tree.root != node:
            node.parent=self.current
            self.dir_tree.insert(node,self.current)
            print(f"drive {node.name} created succ")
        else:
            print(f"drive NOT {node.name} created")


    def cd(self,node:TreeNode):
        if node in self.current.children:
            self.current=node
            self.dir_track.append(node)
            self.go_forward_arrow_stack=[]
            print(f"cd to {self.current.name} succ")
        else:
            print(f"cd to {self.current.name} NOT succ")



    def mkdir(self,node:TreeNode):
        if self.current.depth() >=1 :
            self.parent=self.current
            self.dir_tree.insert(node,self.current)
            print(f"mkdir {node.name} succ")

        else:
            print(f"mkdir {node.name} NOT succ")

    def copy(self,node:TreeNode):
        self.virtual_copy_space=deepcopy(node)


    def paste (self,destny_node:TreeNode):
        if self.virtual_copy_space != None and self.virtual_copy_space not in destny_node.children:
            self.dir_tree.insert(self.virtual_copy_space,destny_node)

        elif self.virtual_copy_space in self.dir_tree.children:
            self.virtual_copy_space.name+=" copy"
            self.dir_tree.insert(self.virtual_copy_space,destny_node)

        else :
            print("unvalid paste")
        #self.virtual_copy_space=None

    def delete(self,node:TreeNode):
        node.parent.children.remove(node)
        del node


    def go_forward_arrow(self):
        if len(self.dir_track) >=1:
            self.dir_track.append(self.go_forward_arrow_stack.pop())
            self.current=self.dir_track[-1]
        else:
            print("we are at top")


    def go_backward_arrow(self):
        if len(self.dir_track) >=2:
            self.go_forward_arrow_stack.append(self.dir_track.pop())
            self.current=self.dir_track[-1]
        else:
            print("we are at This PC")

    def reset_up_arrow(self):
        self.dir_track=[]
        self.dir_track.append(self.dir_tree.root)








ex=FileSystem()
c=TreeNode("C")
ex.create_drive(c)
ex.cd(c)
download=TreeNode("download")
ex.mkdir(download)
ex.cd(download)

print(ex.current)
ex.pwd()

print(download.depth())

print(ex.dir_track[0].disp())