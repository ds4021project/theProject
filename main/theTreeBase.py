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
    def __init__(self, name:str,size=0,type="directory"):
        self.name = name
        self.parent=None
        self.children = []
        self.type=type
        self.size=size

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
        pptree.print_tree(self,'children','name'+' type')


class FileNode(TreeNode):
    "Node of a Tree"
    def __init__(self, name:str,type:str):
        self.name = name
        self.parent=None
        self.children = []
        self.type=type
        self.elemnt = ""


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
    def __init__(self,FileSystem_size:int):
        self.dir_tree=Tree()
        self.dir_tree.root=DirNode("This PC",None)
        self.current=self.dir_tree.root
        self.dir_track=[self.dir_tree.root]
        self.FileSystem_size=FileSystem_size
        self.go_forward_arrow_stack=[]
        self.virtual_copy_space=None
        self.is_cuted=False
        self.inEditMode = False
        self.editFileName = ""
        self.isInCutOrCopy = False
        self.theFirstRun = False

    def pwd(self):
        strer = ""
        theL = []
        for i in self.dir_track:
            print(i.name)
            theL.append(i.name)
            # strer += i.name + "/"
        # print(strer[:-1])
        # print(strer[:-1])
        print(theL)
        return theL
    
    def get_children_dict(self):
        output_dict=dict()
        for i in self.current.children:
            output_dict[i.name]=i.type
        return output_dict
    
    def get_children_list(self):
        output_list=[]
        for i in self.current.children:
            ls=[]
            ls.append(i.name)
            ls.append(i.type)
            output_list.append(ls)
        return output_list
    def getOnlyDirNode(self) :
        output_list=[]
        for i in self.current.children:
            if i.type == "directory" :
                output_list.append(i.name)
        return output_list





    def add_drive(self,node:DirNode):
        if self.current.depth() != 1 and self.FileSystem_size >= node.size:
            node.parent=self.current
            self.dir_tree.insert(node,self.current)
            self.FileSystem_size -= node.size
            print(f"drive {node.name} created succ")
        else:
            print(f"drive NOT {node.name} created")



    def mkdrive(self,name:str,drive_size:int):
            tmp=DirNode(name,drive_size)
            self.add_drive(tmp)


    def name_to_node(self,name:str):
        for i in self.current.children:
            if name==i.name:
                return i



    def cd(self,node:DirNode):
        if node in self.current.children:
            self.current=node
            self.dir_track.append(node)
            self.go_forward_arrow_stack=[]
            print(f"cd to {self.current.name} succ")
        else:
            print(f"cd to {self.current.name} NOT succ")


    def cd_name(self,name:str):
        node=self.name_to_node(name)
        self.cd(node)


    def add_dir(self,node:DirNode):
        if self.current.depth() >=1 :
            self.parent=self.current
            self.dir_tree.insert(node,self.current)
            print(f"add_dir {node.name} succ")

        else:
            self.add_drive(node)
            print(f"add_dir {node.name} NOT succ, add dirver")

    def mkdir(self,name:str):
        tmp=DirNode(name)
        self.add_dir(tmp)
        



    def add_file(self,node:DirNode):
        if self.current.depth() >=1 :
            self.parent=self.current
            self.dir_tree.insert(node,self.current)
            print(f"add_file {node.name} succ")

        else:
            print(f"add_file {node.name} NOT succ")

    def mkfile(self,name:str,type:str):
        tmp=FileNode(name,type)
        self.add_file(tmp)



    def copy(self,node:TreeNode):
        self.virtual_copy_space=deepcopy(node)
    
    def copy_name(self,name:str):
        node=self.name_to_node(name)
        self.copy(node)        




    def paste(self):
        if self.is_cuted==False:
            if self.virtual_copy_space is not None and self.virtual_copy_space not in self.current.children:
                self.dir_tree.insert(self.virtual_copy_space,self.current)


            elif self.virtual_copy_space in self.current.children:
                self.virtual_copy_space=deepcopy(self.virtual_copy_space)
                self.virtual_copy_space.name+=" copy"
                self.dir_tree.insert(self.virtual_copy_space,self.current)

            else :
                print("unvalid paste")
                #self.virtual_copy_space=None
                
        else:   # cut
            self.virtual_copy_space.parent.children.remove(self.virtual_copy_space)
            self.current.add_child(self.virtual_copy_space)
            self.is_cuted=False



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
            if node in self.go_forward_arrow_stack:     
                self.go_forward_arrow_stack.remove(node)
            if node in self.go_forward_arrow_stack:     
                self.go_forward_arrow_stack.remove(node)

            
    def delete_name(self,name:str):
        node=self.name_to_node(name)
        self.delete(node)        


    


    def cut(self, node: TreeNode):
        self.is_cuted=True
        self.virtual_copy_space=node
        
    def cut_name(self,name:str):
        node=self.name_to_node(name)
        self.cut(node)        
    



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
        self.current=self.dir_track[-1]

    def removeDuplicates(self,paths):
        newPathsN = []            
        for path in paths :
            if paths[0] != path :
                newPathsN.append(f"{paths[0]}/{path}")
        newPaths = []            
        for path in newPathsN:
            directories = path.split('/')
            if len(directories) > 1 and directories[-1] == directories[-2]:
                print(directories)
                directories = directories[:-1]
            newPaths.append('/'.join(directories))
        return newPaths
    def getAllDirectoryPaths(self):
        paths = []
        visitedNode = []
        def traverse(node, path):
            if node not in visitedNode :
                if node.type == "directory":
                    visitedNode.append(node)
                    paths.append(path + [node.name])
                for child_name in self.getOnlyDirNode():
                    self.cd_name(child_name)
                    traverse(self.current, path + [child_name])
                    self.go_backward_arrow()
        traverse(self.dir_tree.root, [])
        return self.removeDuplicates(["/".join(path) for path in paths])
    def rename(self,current_name:str, new_name:str):
        node=self.name_to_node(current_name)
        node.name=new_name






"""
ex=FileSystem(100)
c=DirNode("C",20)
d=DirNode("D",10)
ex.add_drive(c)
ex.add_drive(d)
ex.cd(c)
download=DirNode("download")
video=DirNode("video")
ex.add_dir(download)
ex.add_dir(video)
ex.cd(download)
print(ex.current)
ex.pwd()

ex.dir_track[0].disp()

ex.copy(download)
ex.paste(d)
ex.paste(d)
ex.paste(d)
txt=FileNode("hello","txt")
ex.add_file(txt)
ex.dir_track[0].disp()
ex.delete(d)
ex.cut(txt)
ex.paste(video)
ex.dir_track[0].disp()

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