import os
import datetime
class treeDataStructure :
    #write code here
    x = 1
#class node
class Node:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.createdDate = datetime.datetime.now()
        self.modifiedDate = datetime.datetime.now()
        self.children = []
        self.parent = None
        self.isDirectory = False
        self.addrec = None
    #اضافه کردن زیرشاحه به نود
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    #حذف کردن زیرشاخه از نود
    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None
    #پیدا کردن یک نود توسط نامش
    def find_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None
    
class manger :
    #write code here
    x = 1
