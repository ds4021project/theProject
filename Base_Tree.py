import pptree
from copy import deepcopy
from abc import ABC, abstractmethod 

class TreeNode(ABC):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def is_root(self):
            pass
    
    @abstractmethod
    def is_leaf(self):
            pass

    @abstractmethod
    def depth(self):   
            pass


class DirNode(TreeNode):
    "Node of a Tree"
    def __init__(self, name:str,type="directory"):
        self.name = name
        self.parent=None
        self.children = []
        self.type=type

    def __repr__(self):
        return self.name

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False
        

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False


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


class FileNode(TreeNode):
    "Node of a Tree"
    def __init__(self, name:str,type:str):
        self.name = name
        self.parent=None
        self.children = []
        self.type=type


    def __repr__(self):
        return f"{self.name}.{self.type}"
    
    def is_root(self):
            return False

    def is_leaf(self):
            return True

    def depth(self):    # Depth of current node
            return 0


class Tree:
    """
    Tree implemenation as a collection of DirNode objects
    """
    def __init__(self):
       self.root=None
       self.nodes=[]

    def insert(self,node:TreeNode,parent:DirNode):   # Insert a node into tree
        if parent is not None:
            parent.add_child(node)
        else:
            if self.root is None:
                self.root=node
        self.nodes.append(node)

    def search(self,data:str):  # Search and return Node in Tree
        index=[]
        for i in self.nodes:
            if i.name==data:
                index.append(i)
        return index

    def search_startswith(self,data:str):  # Search via startswith and return Node in Tree
        index=[]
        for i in self.nodes:
            if i.name.startswith(data):
                index.append(i)
        return index

    def root(self):
        return self.root
    
class FileSystem:
    """FileSystem class via tree implementation"""
    def __init__(self):
        self.dir_tree=Tree()
        self.dir_tree.root=DirNode("this PC",None)
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


    def create_drive(self,node:DirNode):
        if self.dir_tree.root != node:
            node.parent=self.current
            self.dir_tree.insert(node,self.current)
            print(f"drive {node.name} created succ")
        else:
            print(f"drive NOT {node.name} created")


    def cd(self,node:DirNode):
        if node in self.current.children:
            self.current=node
            self.dir_track.append(node)
            self.go_forward_arrow_stack=[]
            print(f"cd to {self.current.name} succ")
        else:
            print(f"cd to {self.current.name} NOT succ")



    def adddir(self,node:DirNode):
        if self.current.depth() >=1 :
            self.parent=self.current
            self.dir_tree.insert(node,self.current)
            print(f"adddir {node.name} succ")

        else:
            print(f"adddir {node.name} NOT succ")

    def mkdir(self,name:str):
        tmp=DirNode(name)
        self.adddir(tmp)
        

    def addfile(self,node:DirNode):
        if self.current.depth() >=1 :
            self.parent=self.current
            self.dir_tree.insert(node,self.current)
            print(f"addfile {node.name} succ")

        else:
            print(f"addfile {node.name} NOT succ")

    def mkfile(self,name:str,type:str):
        tmp=FileNode(name,type)
        self.addfile(tmp)



    def copy(self,node:TreeNode):
        self.virtual_copy_space=deepcopy(node)


    def paste(self,destiny_node:TreeNode):
        if self.virtual_copy_space is not None and self.virtual_copy_space not in destiny_node.children:
            self.dir_tree.insert(self.virtual_copy_space,destiny_node)


        elif self.virtual_copy_space in destiny_node.children:
            self.virtual_copy_space=deepcopy(self.virtual_copy_space)
            self.virtual_copy_space.name+=" copy"
            self.dir_tree.insert(self.virtual_copy_space,destiny_node)


        else :
            print("unvalid paste")
            #self.virtual_copy_space=None


        """    
        def delete(self, node: TreeNode):   #recursive delete
        if not node.children:
            self.dir_tree.nodes.remove(node)
            node.parent.children.remove(node)
        else:
            for child in node.children.copy():
                self.delete(child)
        """

    def delete(self, node: TreeNode):
        if not node.children:
            if node.parent:
                node.parent.children.remove(node)
            self.dir_tree.nodes.remove(node)
        else:
            for child in node.children.copy():
                self.delete(child)
            if node.parent:
                node.parent.children.remove(node)
            self.dir_tree.nodes.remove(node)

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
c=DirNode("C")
d=DirNode("D")
ex.create_drive(c)
ex.create_drive(d)
ex.cd(c)
download=DirNode("download")
video=DirNode("video")
ex.adddir(download)
ex.adddir(video)
ex.cd(download)
print(ex.current)
ex.pwd()

ex.dir_track[0].disp()

ex.copy(download)
ex.paste(d)
ex.paste(d)
ex.paste(d)
txt=FileNode("hello","txt")
ex.addfile(txt)
ex.dir_track[0].disp()
ex.delete(d)
ex.dir_track[0].disp()
"""
print(type(ex.dir_tree.nodes[-1]))
ex.delete(ex.dir_tree.nodes[-1])


ex.dir_track[0].disp()
print(ex.dir_tree.nodes)

print(ex.dir_tree.search("download copy copy"))


ex.go_backward_arrow()
ex.pwd()
ex.go_backward_arrow()
ex.pwd()

ex.go_forward_arrow()
ex.pwd()
ex.go_forward_arrow()
ex.pwd()

ex.reset_up_arrow()
ex.pwd()
"""