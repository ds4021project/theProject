#requirments
"""
create drive
create dir

copy
paste

goforward_dir

goforward_arrow
gobackward_arrow

delete drive
delete dir


dir list show

working dir from root

"""
class Explorer:

    def __init__(self) :
        self.dir_track=["This PC"]
        self.dir_tree={"This PC":[]}
        self.dir_forward_track_arrow=[]
        self.virtual_copy_space=""

        
    def working_dir(self): 
        return self.dir_track[-1]

    def dir_list(self):
        return self.dir_tree[self.working_dir()]


    def working_dir_from_root(self):
        print("//".join(self.dir_track))
        return "//".join(self.dir_track)


    def create_drive(self,name:str):
        if self.working_dir() == "This PC" :   # This PC  dir
            if name in self.dir_tree[self.working_dir()]:   #repeated drive name
                print("repeated drive")
            else:
                self.dir_tree[name]=[]
                self.dir_tree[self.working_dir()].append(name)            
        else:
            print("normal dir can not create folder")
    

    def mkdir(self, name:str):
        if self.working_dir()=="This PC":   # it is a drive can not mkdir
            print("it is a drive can not mkdir")
            
        else :  #normal dir
            if name in self.dir_tree[self.working_dir()]:   #repeated dir name
                print("repeated folder name")
            else:
                self.dir_tree[name]=[]
                self.dir_tree[self.working_dir()].append(name)



    def goforward_dir(self, name:str):
        if name in self.dir_tree[self.working_dir()] :  #directory exists
            self.dir_track.append(name)
        else:   #dir not exists
            print("dir not exists")
        self.dir_forward_track_arrow=[]
        
            

    def gobackward_arrow(self):
        if len(self.dir_track) > 1:
            self.dir_forward_track_arrow.insert(0,self.dir_track.pop())
        else :  #Already at the root directory
            print("Already at the root directory")    

    def goforward_arrow(self):
        if self.dir_forward_track_arrow:
            self.dir_track.append(self.dir_forward_track_arrow[0])

        else:   #no forward exists
            print("no forward exists")    

    def reset_dir_arrow(self):
        self.dir_track=["This PC"]
        self.dir_forward_track_arrow=[]


    def rmdir(self,name):
        """if name in self.dir_list(self.working_dir()) :
            for i in :
                self.dir_tree.pop(i)
        """
        pass


    def dir_list_show(self):
        ls=self.dir_tree[self.working_dir()]
        for i in ls:
            print(i,end="   ")
        



    def copy(self,origin_dir:str):
        if origin_dir in self.dir_tree :
            self.virtual_copy_space=origin_dir
        else:
            print("origin_dir not exists")    #origin_dir not exists


    def paste(self,destination_dir:str):
        if destination_dir in self.virtual_copy_space:
            self.dir_tree[destination_dir].append(self.virtual_copy_space)
            self.virtual_copy_space=[]
        else:
            print("destination_dir not exists") #destination_dir not exists


ex=Explorer()
ex.create_drive("c")

"""
ex.goforward_dir("c")
ex.mkdir("first")
ex.mkdir("second")
ex.goforward_dir("first")
ex.mkdir("hello3")
ex.goforward_dir("hello3")
ex.gobackward_arrow()


ex.working_dir_from_root()
print(ex.dir_tree)
print(ex.dir_track)
ex.goforward_arrow()
print(ex.dir_tree)
ex.working_dir_from_root()
ex.gobackward_arrow()
ex.working_dir_from_root()
ex.gobackward_arrow()"""