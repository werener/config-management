import json as j


class Vfs:
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
    
    def cd(self, where: str='/'):
        if where == '/' or where == '~':
            self.current_path = ['']
            self.current_dir = self.vfs
            return ""
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
                                return f"cd: {direction}: Not a directory"
                            else:
                                self.current_path.append(direction)
                                self.current_dir = self.current_dir[direction]
                        except:
                            self.current_path, self.current_dir = save_state
                            return f"cd: {direction}: No such file or directory"
        return ""
                    
    def ls(self, path: str="."):
        @staticmethod
        def pretty_dir(s: str):
            try:
                if self.current_dir[s] != "file":
                    return "/"+s
            except:
                raise Exception(f"wrong VFS structure: file {self.current_dir} doesn't have a 'file' tag")
            return s
        save_state = (self.current_path.copy(), self.current_dir.copy())
        
        cd_ = self.cd(path)
        if cd_:
            return cd_.replace("cd", "ls")
                   
        ret = '\n'.join([pretty_dir(o) for o in self.current_dir])
        self.current_path, self.current_dir = save_state
        return ret

    def vfs_save(self, path):
        save_state = (self.current_path.copy(), self.current_dir.copy())
        try:
            with open(path, 'w') as file:
                j.dump(self.vfs, file)
                return ""
        except:
            return "Failed to save VFS"

if __name__ == '__main__':
    vfs = Vfs('./VFS.json')
    
    print('|',vfs.cd("/first"), '|', sep='')
    
    