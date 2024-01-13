import os
import datetime

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

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None

    def find_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

    def find_parent(self):
        return self.parent

    def get_parent_path(self):
        if self.parent is not None:
            return self.parent.get_path() + os.path.sep + self.parent.name
        else:
            return ""

    def get_path(self):
        if self.parent is not None:
            return self.parent.get_path() + os.path.sep + self.name
        else:
            return self.name


class FileSystem:
    def __init__(self):
        self.root = Node("Root")
        self.root.isDirectory = False
        self.part1 = None
        self.part2 = None
        self.part3 = None
        self.part4 = None
        self.num_parts = 0
        self.space_ma = 0

    def create_file_start(self, file_name, size_in_kb, parent_f):
        file_path = f"C:/{file_name}.dsfs"
        file_name = file_name
        size_in_byte = size_in_kb * 1024

        with open(file_path, "wb") as fs:
            fs.write(file_name.encode("utf-8"))
            fs.write(size_in_byte.to_bytes(8, byteorder='big'))
            file_data = bytes([0] * size_in_byte)
            fs.write(file_data)

        file_node = Node(file_name)
        file_node.isDirectory = False
        file_node.size = size_in_kb
        file_node.addrec = file_path
        self.root = file_node

        self.space_ma = size_in_kb

        self.part1 = self.root
        self.part1.isDirectory = True
        self.part1.size = size_in_kb
        self.root.add_child(self.part1)
        self.part1.parent = self.root

    def partition_sf(self, name_partition, partition_size_in_kb):
       
        file_path = f"C:/{self.root.name}/{name_partition}"
        file_name = name_partition
        size_in_byte = partition_size_in_kb * 1024

        file_node = Node(name_partition)
        file_node.isDirectory = False
        file_node.size = partition_size_in_kb
        self.root.add_child(file_node)
        file_node.parent = self.root

    def partition_management(self, name_partition, partition_size_in_kb):
        partition_size_in_byte = partition_size_in_kb * 1024
        mojod = False
        if self.num_parts < 5:
            if partition_size_in_byte < self.space_ma:
                for child in self.root.children:
                    if name_partition == child.name:
                        print("!!!The entered name is available!!!")
                        mojod = True
                        break
                if not mojod:
                    self.part1.size -= partition_size_in_byte
                    self.space_ma += partition_size_in_byte
                    self.num_parts += 1
                    self.partition_sf(name_partition, partition_size_in_kb)
            else:
                print("!!!The imported volume is more than the allowed amount!!!")
        else:
            print("You cannot add a partition\r\n!!!The number of partitions has reached the limit!!!")

    def add_directory(self, name_dir, parent):
        partition_path = parent.addrec
        folder_name = name_dir
        folder_path = os.path.join(partition_path, folder_name)
        folder = os.path.join(partition_path, folder_name)
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            count = 0
            for child in parent.children:
                if name_dir == child.name:
                    count += 1
                    folder_name += f"{count}"
            os.makedirs(folder)

        new_dir = Node(folder_name)
        new_dir.isDirectory = True
        new_dir.addrec = folder_path
        parent.add_child(new_dir)
