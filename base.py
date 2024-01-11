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
        self.dir_track=["/"]
        self.dir_tree={"/":[]}
        self.dir_forward_track_arrow=[]

        
    def working_dir(self): 
        return self.dir_track[-1]

    def dir_list(self):
        return self.dir_tree[self.working_dir()]


    def working_dir_from_root(self):
        print("/".join(self.dir_track[1:]))
        return "/".join(self.dir_track[1:])


    def create_drive(self,name:str):
        if self.working_dir() == '/' :   #normal dir
            self.dir_tree[name]=[]
            self.dir_tree[self.working_dir()].append(name)            
        else:
            print("normal dir can not create folder")
    

    def mkdir(self, name:str):
        if self.working_dir()=="/":   #
            print("it is a drive can not mkdir")
            
        else :  #normal dir
            self.dir_tree[name]=[]
            self.dir_tree[self.working_dir()].append(name)



    def goforward_dir(self, name:str):
        if name in self.dir_tree[self.working_dir()] :  #directory exists
            self.dir_track.append(name)
        else:   #dir not exists
            #print("dir not exists")
            pass

    def gobackward_arrow(self):
        if len(self.dir_track) > 1:
            self.dir_forward_track_arrow.append(self.dir_track.pop())
        else :
            pass    #Already at the root directory

    def goforward_arrow(self):
        if self.dir_forward_track_arrow:
            self.dir_track.append(self.dir_forward_track_arrow[-1])

        else:
            pass    #no forward exists

    def reset_dir(self):
        self.dir_track=["/"]
        self.dir_forward_track_arrow=[]


    def rmdir(self,name):
        """if name in self.dir_list(self.working_dir()) :
            for i in :
                self.dir_tree.pop(i)
        """
        pass


    def dir_list_show(self,name:str):
        ls=self.dir_tree[self.working_dir()]
        for i in ls:
            print(i,end="   ")
        



    def copy(self):
        pass

    def paste(self):
        pass


ex=Explorer()
ex.create_drive("c")
print(ex.dir_tree)
print(ex.dir_track)

ex.goforward_dir("c")
ex.mkdir("hello")
ex.goforward_dir("hello")
print(ex.dir_tree)
ex.working_dir_from_root()