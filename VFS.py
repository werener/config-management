import json as j
import base64


class Vfs:
    current_path: list

    current_dir: dict
    vfs: dict

    def __init__(self, path_to_VFS_file: str):
        self.current_path = [""]
        try:
            with open(path_to_VFS_file) as vfs_json:
                self.vfs = j.load(vfs_json)
            self.current_dir = self.vfs
        except Exception as e:
            raise Exception("Provided path for VFS doesn't exist")

    def len(self):
        return len(self.get_path())

    def get_path(self):
        return "~" + "/".join(self.current_path)

    def cd(self, where: str = "/"):
        if where == "/" or where == "~":
            self.current_path = [""]
            self.current_dir = self.vfs
            return ""
        where = where.removesuffix("/")
        save_state = (self.current_path.copy(), self.current_dir.copy())
        for direction in where.split("/"):
            match direction:
                case "":
                    self.current_path = [""]
                    self.current_dir = self.vfs
                case ".":
                    pass
                case "..":
                    if self.current_path[-1] == "":
                        self.current_dir = self.vfs
                    else:
                        self.current_path.pop(-1)
                        self.cd("/".join(self.current_path))
                case _:
                    try:
                        if type(self.current_dir[direction]) == list:
                            self.current_path, self.current_dir = save_state
                            return f"cd: {direction}: Not a directory"
                        else:
                            self.current_path.append(direction)
                            self.current_dir = self.current_dir[direction]
                    except:
                        self.current_path, self.current_dir = save_state
                        return f"cd: {direction}: No such file or directory"
        return ""

    def ls(self, path: str = "."):

        @staticmethod
        def pretty_dir(s: str):
            try:
                if type(self.current_dir[s]) != list:
                    return "/" + s
            except:
                raise Exception(
                    f"wrong VFS structure: file {self.current_dir} doesn't have a 'file' tag or content"
                )
            return s

        save_state = (self.current_path.copy(), self.current_dir.copy())

        cd_ = self.cd(path)
        if cd_:
            return cd_.replace("cd", "ls")

        ret = "\n".join([pretty_dir(o) for o in self.current_dir])
        self.current_path, self.current_dir = save_state
        return ret

    def vfs_save(self, path):

        try:
            with open(path, "w") as file:
                j.dump(self.vfs, file)
                return ""
        except:
            return "Failed to save VFS"

    def vfs_load(self, path):
        try:
            with open(path) as vfs_json:
                self.vfs = j.load(vfs_json)
                self.current_dir = self.vfs
                return f"VFS succesfully loaded"
        except:
            return "Provided path for VFS doesn't exist"

    def tail(self, path: str):
        save_state = (self.current_path.copy(), self.current_dir.copy())
        path = path.removesuffix("/")
        file = path[path.rfind("/") + 1:]
        path = path.replace(file, "")
        if path:
            cd_ = self.cd(path)
            if cd_:
                return cd_.replace("cd", "tail")

        try:
            if type(self.current_dir[file]) == list:
                try:
                    content = self.current_dir[file][2]
                except:
                    ret = f"tail: {file} doesn't have content"
                try:
                    decoded_content = base64.b64decode(content).decode("utf-8")
                except:
                    ret = f"tail: error decoding contents of {file}"
                ret = "\n".join(decoded_content.split("\n")[-10:])
                self.current_path, self.current_dir = save_state
                return ret
            else:
                self.current_path, self.current_dir = save_state
                return f"tail: {file}: is a directory, not a file"
        except:
            self.current_path, self.current_dir = save_state
            return f"tail: {file}: No such file"

    def rev(self, path: str):
        save_state = (self.current_path.copy(), self.current_dir.copy())
        path = path.removesuffix("/")
        file = path[path.rfind("/") + 1:]
        path = path.replace(file, "")
        if path:
            cd_ = self.cd(path)
            if cd_:
                return cd_.replace("cd", "rev")

        try:
            if type(self.current_dir[file]) == list:
                try:
                    content = self.current_dir[file][2]
                except:
                    ret = f"rev: {file} doesn't have content"
                try:
                    decoded_content = base64.b64decode(content).decode("utf-8")
                except:
                    ret = f"rev: error decoding contents of {file}"
                ret = "\n".join(
                    map(lambda s: s[::-1], decoded_content.split("\n")))

                self.current_path, self.current_dir = save_state
                return ret
            else:
                self.current_path, self.current_dir = save_state
                return f"rev: {file}: is a directory, not a file"
        except:
            self.current_path, self.current_dir = save_state
            return f"rev: {file}: No such file"

    def wc(self, path: str):
        save_state = (self.current_path.copy(), self.current_dir.copy())
        path = path.removesuffix("/")
        file = path[path.rfind("/") + 1:]
        path = path.replace(file, "")
        if path:
            cd_ = self.cd(path)
            if cd_:
                return cd_.replace("cd", "wc")
        try:
            if type(self.current_dir[file]) == list:
                try:
                    content = self.current_dir[file][2]
                except:
                    ret = f"wc: {file} doesn't have content"
                try:
                    decoded_content = base64.b64decode(content).decode("utf-8")
                except:
                    ret = f"wc: error decoding contents of {file}"
                ret = f"""lines: {len(decoded_content.split('\n'))}
words: {len(decoded_content.replace('\n', ' ').replace('\t', ' ').split())}
bytes: {len(content)}
chars: {len(decoded_content)}"""

                self.current_path, self.current_dir = save_state
                return ret
            else:
                self.current_path, self.current_dir = save_state
                return f"wc: {file}: is a directory, not a file"
        except:
            self.current_path, self.current_dir = save_state
            return f"wc: {file}: No such file"

    def cat(self, path: str):
        save_state = (self.current_path.copy(), self.current_dir.copy())
        path = path.removesuffix("/")
        file = path[path.rfind("/") + 1:]
        path = path.replace(file, "")
        if path:
            cd_ = self.cd(path)
            if cd_:
                return cd_.replace("cd", "cat")
        try:
            if type(self.current_dir[file]) == list:
                try:
                    content = self.current_dir[file][2]
                except:
                    ret = f"cat: {file} doesn't have content"
                try:
                    decoded_content = base64.b64decode(content).decode("utf-8")
                except:
                    ret = f"cat: error decoding contents of {file}"
                ret = f" Title: {self.current_dir[file][0]}\n Owner: {self.current_dir[file][1]}\n{decoded_content}"

                self.current_path, self.current_dir = save_state
                return ret
            else:
                self.current_path, self.current_dir = save_state
                return f"cat: {file}: is a directory, not a file"
        except:
            self.current_path, self.current_dir = save_state
            return f"cat: {file}: No such file"

    def chown(self, path: str, new_owner: str):
        save_state = (self.current_path.copy(), self.current_dir.copy())
        path = path.removesuffix("/")
        file = path[path.rfind("/") + 1:]
        path = path.replace(file, "")
        if path:
            cd_ = self.cd(path)
            if cd_:
                return cd_.replace("cd", "chown")
        try:
            if type(self.current_dir[file]) == list:
                try:
                    ret = f"owner succesfully changed from {self.current_dir[file][1]} to {new_owner}"
                    self.current_dir[file][1] = new_owner
                except:
                    ret = f"chown: {file} doesn't have an owner"

                self.current_path, self.current_dir = save_state
                return ret
            else:
                self.current_path, self.current_dir = save_state
                return f"chown: {file}: is a directory, not a file"
        except:
            self.current_path, self.current_dir = save_state
            return f"chown: {file}: No such file"

    def ls(self, path: str = "."):

        @staticmethod
        def pretty_dir(s: str):
            try:
                if type(self.current_dir[s]) != list:
                    return "/" + s
            except:
                raise Exception(
                    f"wrong VFS structure: file {self.current_dir} doesn't have a 'file' tag or content"
                )
            return s

        save_state = (self.current_path.copy(), self.current_dir.copy())

        cd_ = self.cd(path)
        if cd_:
            return cd_.replace("cd", "ls")

        ret = "\n".join([pretty_dir(o) for o in self.current_dir])
        self.current_path, self.current_dir = save_state
        return ret

    def rm(self, path: str):
        save_state = (self.current_path.copy(), self.current_dir.copy())
        path = path.removesuffix("/")
        file = path[path.rfind("/") + 1:]
        path = path.replace(file, "")
        if path:
            cd_ = self.cd(path)
            if cd_:
                return cd_.replace("cd", "rm")

        try:
            print(self.current_dir[file], sep = '\n')
            if type(self.current_dir[file]) == list:
                del self.current_dir[file]
                print('\n\n',self.vfs, sep = '\n')               
                
            else:
                self.current_path, self.current_dir = save_state
                return f"rm: {file}: is a directory, not a file"
        except Exception as e:
            self.current_path, self.current_dir = save_state
            return f"rm: {file}: No such file"

if __name__ == "__main__":
    vfs = Vfs("./VFS.json")
    vfs.cd("/first/for_txt/")
    print(vfs.chown("file2.txt", "admin"))
    my_string = ""
    print(base64.b64encode(my_string.encode("utf-8")))
