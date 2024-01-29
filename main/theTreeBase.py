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
    "Node of a Tree as directory"
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

    def disp(self):     #implemented via pptree package
        pptree.print_tree(self,'children','name'+' type')


class FileNode(TreeNode):
    "Node of a Tree as file"
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
    Tree implemenation as a collection of DirNode and FileNode objects
    """
    def __init__(self):
       self.root=None
       self.nodes=[]

    def insert(self,node:TreeNode,parent:DirNode):   # Insert a node into tree set it as root or node
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


    
class FileSystem:
    """FileSystem class via tree implementation"""
    def __init__(self,FileSystem_size:int):

        # initializing General tree
        self.dir_tree=Tree()
        self.dir_tree.root=DirNode("This PC",None)
        self.current=self.dir_tree.root

        self.dir_track=[self.dir_tree.root]     # dir_track save our route for This PC
        
        self.FileSystem_size=FileSystem_size   # size of our FileSystem     
        self.__go_forward_arrow_stack=[]      # Used for tracking backward_arrow

        # copy and paste attributes
        self.__virtual_copy_space=None
        self.__is_cuted=False
        self.isInCutOrCopy = False
        self.theFirstRun = False





    
    # -------------------------------- Accessor Methods -------------------------------- #

    def name_to_node(self,name:str):    # Convert name to NOde in current directory
        for i in self.current.children:
            if name==i.name:
                return i
        return None
    
    def show(self): # Show tree in tree view
        self.dir_tree.root.disp()



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
    
    
    def get_children_dict(self):    # Return Node children in dict 
        output_dict=dict()
        for i in self.current.children:
            output_dict[i.name]=i.type
        return output_dict
    
    
    def get_children_list(self):    # Return Node children in list 
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


    # -------------------------------- Modifier Methods  -------------------------------- #

    
    def add_drive(self, node: DirNode):      # Adding drive Node to tree
        if self.current.depth() == 0 and self.FileSystem_size >= node.size:
            # Check if a drive with the same name already exists
            existing_node = self.name_to_node(node.name)
            if existing_node:
                count = 1
                new_name = f"{node.name}_{count}"
                # Find a new name with a unique suffix
                while self.name_to_node(new_name) is not None:
                    count += 1
                    new_name = f"{node.name} ({count})"
                node.name = new_name

            self.dir_tree.insert(node, self.current)
            self.FileSystem_size -= node.size
            print(f"drive {node.name} created successfully")
            return True
        else:
            print(f"drive {node.name} creation Failed")
            return False
    def mkdrive(self,name:str,drive_size:int):      # Create and add drive Node to tree via name
            tmp=DirNode(name,drive_size)
            return self.add_drive(tmp)




    def add_dir(self, node: DirNode):
        if self.current.depth() >= 1:
            # Check if a directory with the same name already exists
            existing_node = self.name_to_node(node.name)
            if existing_node:
                count = 1
                new_name = f"{node.name} ({count})"
                # Find a new name with a unique suffix
                while self.name_to_node(new_name) is not None:
                    count += 1
                    new_name = f"{node.name} ({count})"
                node.name = new_name

            self.dir_tree.insert(node, self.current)    # Adding new directory
            print(f"add_dir {node.name} was successful")
        else:
            print(f"add_dir {node.name} Failed")

    def mkdir(self,name:str):       # Create and add directory Node to tree via name
        tmp=DirNode(name)
        self.add_dir(tmp)
        


    def add_file(self,node:DirNode):        # Adding file Node to tree
        if self.current.depth() >=1 :

            # Check if a directory with the same name already exists
            existing_node = self.name_to_node(node.name)
            if existing_node:
                count = 1
                new_name = f"{node.name} ({count})"

                # Find a new name with a unique suffix
                while self.name_to_node(new_name) is not None:
                    count += 1
                    new_name = f"{node.name} ({count})"
                node.name = new_name

            self.dir_tree.insert(node,self.current)
            print(f"add_file {node.name} was successful")
        else:
            print(f"add_file {node.name} Failed")

    def mkfile(self,name:str,type:str):     # Create and add file Node to tree via name
        tmp=FileNode(name,type)
        self.add_file(tmp)




    def copy(self,node:TreeNode):   # Add TreeNode to virtual_copy_space
        self.__virtual_copy_space=node
    
    def copy_name(self,name:str):   # Add TreeNode to virtual_copy_space via name
        node=self.name_to_node(name)
        self.copy(node)        


    """
    here paste method can use for both copy and paste methods

    to avoiding multiple reference to a node we used hard copy
    """

    def paste(self):
        if not self.__is_cuted: # Happens when we are in copy mode
            # Paste for first time
            if self.__virtual_copy_space is not None and self.__virtual_copy_space not in self.current.children:
                copied_node = deepcopy(self.__virtual_copy_space)
                new_name = copied_node.name
                count = 1

                # Add a suffix if the node with the same name already exists
                while self.name_to_node(new_name) is not None:
                    new_name = f"{copied_node.name} ({count})"
                    count += 1

                copied_node.name = new_name
                self.dir_tree.insert(copied_node, self.current)

            elif self.__virtual_copy_space in self.current.children:    # We have multiple paste
                copied_node = deepcopy(self.__virtual_copy_space)
                new_name = copied_node.name
                count = 1

                # Add a suffix if the node with the same name already exists
                while self.name_to_node(new_name) is not None:
                    new_name = f"{copied_node.name} ({count})"
                    count += 1

                copied_node.name = new_name
                self.dir_tree.insert(copied_node, self.current)

            else:
                print("Invalid paste: virtual_copy_space is not set.")

        else:  # Happens when we are in cut mode

            self.__virtual_copy_space.parent.children.remove(self.__virtual_copy_space)
            new_name = self.__virtual_copy_space.name
            count = 1

            # Add a suffix if the node with the same name already exists
            while self.name_to_node(new_name) is not None:
                new_name = f"{self.__virtual_copy_space.name}_{count}"
                count += 1

            self.__virtual_copy_space.name = new_name
            self.current.add_child(self.__virtual_copy_space)
            self.__is_cuted = False



    """
    Here delete implemented recursively
    """

    def delete(self, node: TreeNode):
        # Base case
        if not node.children: # Happens when we are at external Node
            if node.parent:
                node.parent.children.remove(node)
                if node in self.__go_forward_arrow_stack:   # Deleting reference in __go_forward_arrow_stack
                    self.__go_forward_arrow_stack.remove(node)
                if node in self.dir_track:  # Deleting reference in dir_track
                    self.dir_track.remove(node)
            self.dir_tree.nodes.remove(node) # Deleting Node in tree

        # Recursion case
        else:   # Happens when we are at internal Node
            for child in node.children.copy():
                self.delete(child)
            if node.parent:
                node.parent.children.remove(node)
                if node in self.__go_forward_arrow_stack:   # Deleting reference in __go_forward_arrow_stack
                    self.__go_forward_arrow_stack.remove(node)
                if node in self.dir_track:  # Deleting reference in dir_track
                    self.dir_track.remove(node)
            self.dir_tree.nodes.remove(node)    # Deleting Node in tree
        
        if node in self.__go_forward_arrow_stack:   # Update __go_forward_arrow_stack after deletion
            self.__go_forward_arrow_stack.remove(node)

            
    def delete_name(self,name:str): # Deleting via name
        node=self.name_to_node(name)
        self.delete(node)        



    
    def cut(self, node: TreeNode):
        self.__is_cuted=True    # This attribute tells paste method diffrance between copy and cut
        self.__virtual_copy_space=node
        
    def cut_name(self,name:str):
        node=self.name_to_node(name)
        self.cut(node)     



    def rename(self,current_name:str, new_name:str):    # Rename a node
        node=self.name_to_node(current_name)
        node.name=new_name


    def save(self):     # Save changes and quit
        import pickle
        with open ("FileExplorer.pickle","wb") as data:
            pickle.dump(self,data)
        

    


    # -------------------------------- Navigation Methods  -------------------------------- #


    def __cd__(self,node:DirNode):  # Will change directory via Node
        if node in self.current.children:
            self.current=node
            self.dir_track.append(node)
            if node not in self.__go_forward_arrow_stack:
                self.__go_forward_arrow_stack=[]
            print(f"cd to {self.current.name} was successful")
        else:
            print(f"cd to {self.current.name} Failed")


    def cd_name(self,name:str):# Will change directory via name

        if name =="..":     # Will implement backward navigation
            self.go_backward_arrow()
        else:
            node=self.name_to_node(name)
            self.__cd__(node)
    
    def __removeDuplicates__(self,paths):
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
        return self.__removeDuplicates__(["/".join(path) for path in paths])
    
    def rename(self,current_name:str, new_name:str):
        node=self.name_to_node(current_name)
        node.name=new_name

    def go_forward_arrow(self): # Navigation to forward

        if len(self.__go_forward_arrow_stack) :
            self.dir_track.append(self.__go_forward_arrow_stack.pop())  # Pop last directory from go_forward_arrow_stack and append it to dir_track
            self.current=self.dir_track[-1] # Setting current directory
        else:
            print("we are at top")


    def go_backward_arrow(self):    # Navigation to backward
        if len(self.dir_track) >=2:
            self.__go_forward_arrow_stack.append(self.dir_track.pop()) # Push last directory to go_forward_arrow_stack
            self.current=self.dir_track[-1]
        else:
            print("we are at This PC")


    def reset_up_arrow(self):   # Navigate us to This PC
        self.dir_track=[]
        self.dir_track.append(self.dir_tree.root)
        self.current=self.dir_track[-1]


"""ex=start()
ex.show()"""


"""
ex.mkdrive("C",10)
ex.mkdrive("D",10)
print(ex.dir_tree.nodes)
ex.cd_name("D")
ex.mkdir("video")
ex.mkdir("download")
ex.mkdir("hello")


ex.copy_name("video")
ex.paste()

ex.paste()

ex.copy_name("video")
ex.paste()
ex.copy_name("video")
ex.paste()
ex.paste()
ex.dir_track[0].disp()

ex.cd_name("video")

ex.go_backward_arrow()
ex.go_backward_arrow()
ex.pwd()
ex.delete_name("D")
ex.go_forward_arrow()
ex.go_forward_arrow()

print(ex.dir_track)
ex.delete_name("C")
ex.dir_track[0].disp()
ex.show()
ex.save()

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
ex.paste()
ex.paste()
ex.paste()
txt=FileNode("hello","txt")
ex.add_file(txt)
ex.dir_track[0].disp()
ex.delete(d)
ex.cut(txt)
ex.paste()
ex.dir_track[0].disp()

ex.go_backward_arrow()
ex.go_backward_arrow()
ex.pwd()
#ex.delete_name("C")
ex.go_forward_arrow()
ex.dir_track[0].disp()
ex.pwd()
ex.go_forward_arrow()
ex.go_forward_arrow()

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