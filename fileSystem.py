

class File:
    
    def __init__(self, name:str) -> None:
        self.name = name
        self.__content = ""

    def __str__(self):
        return f"File: {self.name}"

    def read(self):
        return self.__content
    
    def write(self,content):
        self.__content = content
        
    def append(self,content):
        self.__content += content


class Directory:
    
    def __init__(self,name:str) -> None:
        self.name = name
        self.__files = {}
        self.__directories = {}
    
    def __str__(self) -> str:
        return f"Directory: {self.name}"
    
    def add_file(self,file_name:str) -> None:
        if not isinstance(file_name,str):
            raise ValueError("Invalid File")
        if file_name in self.__files:
            raise ValueError("File already exists")
        self.__files[file_name] = File(file_name)
    
    def add_directory(self,directory_name:str) -> None:
        if not isinstance(directory_name,str):
            raise ValueError("Invalid Directory")
        if directory_name in self.__directories:
            raise ValueError("Directory already exists")
        self.__directories[directory_name] = Directory(directory_name)
    
    def list_directory(self):
        print('\n'.join([f"File: {file}" for file in self.__files]) +  '\n' + '\n'.join([f"Directory: {directory}" for directory in self.__directories]))
        
    def search_files(self,file_name:str):
        return self.__files.get(file_name)
    
    def search_directories(self,directory_name:str):
        return self.__directories.get(directory_name)
    
    def create_tree(self,tabs=0):
        print(self.name)
        for directory in self.__directories:
            print(f"{"\t"*tabs}|--",end="")
            self.__directories[directory].create_tree(tabs+1)
        for file in self.__files:
            print(f"{"\t"*tabs}|--{file}")

class FileSystem:
    
    def __init__(self) -> None:
        self.ROOT = Directory("~")
        self.PATH = [self.ROOT]
        
    def __path_helper(self,path_arr,idx,temp_path,dir_only=False):
        if idx == len(path_arr):
            return
        if path_arr[idx] == "..":
            if temp_path[-1] == self.ROOT:
                raise ValueError("Can't go back from root directory")
            temp_path.pop()
        elif path_arr[idx] != ".":
            directory = temp_path[-1].search_directories(path_arr[idx]) or (not dir_only and temp_path[-1].search_files(path_arr[idx]))
            if directory is not None:
                temp_path.append(directory)
            else:
                raise ValueError("Invalid Path")
        self.__path_helper(path_arr,idx+1,temp_path,dir_only)
        
    def __get_object_from_path(self,path:str):
        path_arr = path.split("/")
        temp_path = self.PATH.copy()
        try:
            self.__path_helper(path_arr,0,temp_path)
            return temp_path[-1]
        except ValueError as e:
            print(e)
    
    def mkdir(self,directory_name:str) -> None:
        try:
            self.PATH[-1].add_directory(directory_name)
        except ValueError as e:
            print(e)
        
    def touch(self,file_name:str) -> None:
        try:
            self.PATH[-1].add_file(file_name)
        except ValueError as e:
            print(e)
    
    def cd(self,path:str)->None:
        path_arr = path.split("/")
        temp_path = self.PATH.copy()
        try:
            self.__path_helper(path_arr,0,temp_path,dir_only=True)
            self.PATH = temp_path
        except ValueError as e:
            print(e)  
        
    def ls(self,path:str=None):
        if path is not None:
            directory = self.__get_object_from_path(path)
            if isinstance(directory,Directory):
                directory.list_directory()
            else:
                print("Can't List Directory")
        else:
            self.PATH[-1].list_directory()
    
    def pwd(self):
        directory = '/'.join([directory.name for directory in self.PATH])
        return directory
        
    def cp(self,source:str,destination:str):
        
        source_obj = self.__get_object_from_path(source)
        destination_obj = self.__get_object_from_path(destination)
        
        if isinstance(source_obj,File) and isinstance(destination_obj,Directory):
            destination_obj.add_file(source_obj.name)
        elif isinstance(source_obj,Directory) and isinstance(destination_obj,Directory):
            destination_obj.add_directory(source_obj.name)
        else:
            print("Can't Copy")
            
    def search(self,name:str):
        return self.PATH[-1].find(name)
    
    def tree(self):
        self.PATH[-1].create_tree()
    
def main():
    fs = FileSystem()
    fs.pwd()
    while(True):
        command = input(fs.pwd() + " > ")
        if command == "exit":
            break
        command = command.split()
        try:
            if command[0] == "mkdir":
                fs.mkdir(command[1])
            elif command[0] == "touch":
                fs.touch(command[1])
            elif command[0] == "cd":
                fs.cd(command[1])
            elif command[0] == "ls":
                if len(command) == 1:
                    fs.ls()
                else:
                    fs.ls(command[1])
            elif command[0] == "pwd":
                print(fs.pwd())
            elif command[0] == "cp":
                fs.cp(command[1],command[2])
            elif command[0] == "tree":
                fs.tree()
            else:
                continue
        except IndexError:
            print("Invalid Command")
            continue
    
    
if __name__ == "__main__":
    main()
    