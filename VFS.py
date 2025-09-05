import json as j


class VFS:
    current_path: list

    path_to_VFS: str
    
    current_dir: dict
    vfs: dict

    def __init__(self, path_to_VFS_file: str):
        self.current_path = ['']
        
        self.path_to_VFS = path_to_VFS_file
        try:
            with open(path_to_VFS_file) as vfs_json:
                self.vfs = j.load(vfs_json)
            self.current_dir = self.vfs
        except Exception as e:
            raise Exception('Provided path for VFS doesn\'t exist')

    def len(self):
        return len(self.get_path())
    
    def get_path(self):
        return "~" + '/'.join(self.current_path)
    
    def cd(self, where: str):
        if where == '/' or where == '~':
            self.current_path = ['']
            self.current_dir = self.vfs
            return (False, "")
        where = where.removesuffix('/')
        save_state = (self.current_path.copy(), self.current_dir.copy())
        for direction in where.split('/'):
            match direction:
                case '':
                    self.current_path = ['']
                    self.current_dir = self.vfs
                case '.':
                    pass
                case '..':
                    if self.current_path[-1] == '':
                        self.current_dir = self.vfs
                    else:
                        self.current_path.pop(-1)
                        self.cd('/'.join(self.current_path))
                case _:
                        try:
                            if self.current_dir[direction] == "file":
                                self.current_path, self.current_dir = save_state
                                return (True, f"cd: {direction}: Not a directory")
                            else:
                                self.current_path.append(direction)
                                self.current_dir = self.current_dir[direction]
                        except:
                            self.current_path, self.current_dir = save_state
                            return (True, f"cd: {direction}: No such file or directory")
        return (False, "")
                    
    def ls(self, path="."):
        save_state = (self.current_path.copy(), self.current_dir.copy())
        
        cd_ = self.cd(path)
        if cd_[0]:
            return (cd_[0], cd_[1].replace("cd", "ls"))
                   
        ret = '\n'.join([o for o in self.current_dir])
        self.current_path, self.current_dir = save_state
        return ret


if __name__ == '__main__':
    vfs = VFS('./VFS.json')
    print(vfs.vfs)
    
    vfs.cd('/root')
    print(vfs.get_path())
    
    print("-"*7)
    print(vfs.ls("/root/"))
    
    