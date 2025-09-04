import json as j


class VFS:
    current_path: list

    path_to_VFS: str
    vfs: dict

    def __init__(self, path_to_VFS_file: str, current_path='/'):
        self.current_path = ['~']
        temp = current_path.\
            replace('\\', '/').\
            replace('~','').\
            removeprefix('/').\
            removesuffix('/')
        if temp.split()[0]:
            self.cd(temp)

        self.path_to_VFS = path_to_VFS_file
        try:
            with open(path_to_VFS_file) as vfs_json:
                self.vfs = j.load(vfs_json)
        except Exception as e:
            if e == Exception(
                    f"No such file or directory: '{path_to_VFS_file}'"):
                raise Exception('Provided path for VFS doesn\'t exist')
            else:
                raise Exception('Unknown error during VFS import')

    def len(self):
        return len(self.get_path())
    def get_path(self):
        return '/'.join(self.current_path)
    
    def cd(self, where: str):
        if where == '/' or where == '~':
            self.current_path = [self.get_root()]
            return

        for direction in where.split('/'):
            match direction:
                case '.':
                    pass
                case '..':
                    if self.current_path[-1] == '~':
                        pass
                    else:
                        self.current_path.pop(-1)

                case _:
                    self.current_path.append(direction)

    def get_root(self):
        try:
            return self.current_path[0]
        except Exception as e:
            if e == Exception('list index out of range'):
                return '~'
            else:
                raise Exception('no root')


if __name__ == '__main__':
    vfs = VFS('./VFS.json', '123/./123/././as')
    print(vfs.get_path())
    vfs.cd('anus/penis')
    print(vfs.get_path())
    vfs.cd('/')
    print(vfs.get_path())
    vfs.cd('govno')
    print(vfs.get_path())
    print(vfs.len())