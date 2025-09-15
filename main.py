import tkinter as tk
from tkinter import ttk
import json
import os, platform, sys, socket
import argv_handling
from VFS import Vfs

LOGIN = os.getlogin()
HOSTNAME = socket.gethostname()
CURRENT_SYSTEM = platform.system()
TERMINAL_HIDDEN = True

PATHS = argv_handling.handle_args()


def get_startup_script():
    path = PATHS["script"]
    if path:
        with open(path, "r") as suf:
            return [x.removesuffix("\n") for x in suf]
    else:
        return []


def gui():
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 512

    FONT = "TkFixedFont"
    global TERMINAL_HIDDEN
    root = tk.Tk()

    if root:
        root.configure(background="black", padx=3, pady=4),
        root.title(f"{LOGIN}@{HOSTNAME}: {vfs.get_path()}")
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    terminal = tk.Label(
        root,
        highlightthickness=0,
        text="",
        pady=0,
        padx=0,
        anchor="nw",
        background="black",
        justify="left",
        borderwidth=0,
        width=WINDOW_WIDTH,
        font=FONT,
        foreground="white",
    )
    container = tk.Frame(
        highlightthickness=0,
        borderwidth=0,
        pady=0,
        background="red",
    )
    prefix = tk.Label(
        container,
        borderwidth=0,
        width=0,
        padx=0,
        anchor="nw",
        background="black",
        justify="left",
        foreground="lime",
        font=FONT,
        text=f"{LOGIN}@{HOSTNAME}: {vfs.get_path()}$",
    )
    input_field = tk.Entry(
        container,
        highlightthickness=0,
        font=FONT,
        justify="left",
        background="black",
        foreground="white",
        borderwidth=0,
        selectbackground="white",
        selectforeground="black",
        insertbackground="white",
        insertborderwidth=2,
        insertwidth=3,
        insertofftime=0,
        width=WINDOW_WIDTH,
    )

    def set_new_working_dir():
        prefix["text"] = f"{LOGIN}@{HOSTNAME}: {vfs.get_path()}$"
        prefix["width"] = len(prefix["text"]) + 1
        input_field["width"] = WINDOW_WIDTH - len(prefix["text"])

    def unhide_terminal():
        global TERMINAL_HIDDEN
        if TERMINAL_HIDDEN:
            TERMINAL_HIDDEN = False
            container.pack_forget()

            terminal.pack(
                side="top",
            )

            container.pack(
                side="top",
            )

            prefix.pack(in_=container, side="left")
            input_field.pack(
                in_=container,
                side="left",
            )

    def add_to_terminal(inp, with_login=False):
        if with_login:
            if terminal["text"]:
                terminal["text"] += f"\n{LOGIN}@{HOSTNAME}: {vfs.get_path()}$ {inp}"
            else:
                terminal["text"] += f"{LOGIN}@{HOSTNAME}: {vfs.get_path()}$ {inp}"
        else:
            if inp:
                terminal["text"] += f"\n{inp}"

    def parse_args(inp=""):
        if inp:
            inp = inp.replace("'", '"')
        else:
            inp = input_field.get().replace("'", '"')
        args = []
        try:
            command = inp.split()[0]
            comma_args, comma_open, buffer = [], False, ""

            for symbol in inp:
                if symbol == '"':
                    if comma_open:
                        comma_open = False
                        comma_args.append(f'"{buffer}"')
                        buffer = ""
                    else:
                        comma_open = True
                else:
                    if comma_open:
                        buffer += symbol

            if comma_open:
                add_to_terminal("unterminated comma")
                return "unterminated_comma_mistake\1\2"
            # in case command is made of several words, i.e. 'good cd' should be a command {good cd}
            if comma_args and (command in comma_args[0]):
                command = comma_args[0].removeprefix('"').removesuffix('"')
            elif comma_args:
                args.append(comma_args[0].removeprefix('"').removesuffix('"'))
                inp = inp.replace(comma_args[0], "")

            for arg in comma_args[1:]:
                args.append(arg.removeprefix('"').removesuffix('"'))
                inp = inp.replace(arg, "")
            args += inp.split()[1:]
        except Exception as e:
            command = ""
            print("Error occured:", e)
        return (command or None, args or [])

    def handle_args(command_args):
        # Command implementation
        command, args = command_args
        match command:
            case None:
                pass
            case "exit":
                root.destroy()
            case "ls":
                match len(args):
                    case 0:
                        add_to_terminal(vfs.ls())
                    case 1:
                        add_to_terminal(vfs.ls(args[0]))
                    case _:
                        for arg in args:
                            add_to_terminal(f" {arg}:")
                            add_to_terminal(vfs.ls(arg))
            case "cd":
                match len(args):
                    case 0:
                        add_to_terminal(vfs.cd())
                        set_new_working_dir()
                    case 1:
                        add_to_terminal(vfs.cd(args[0]))
                        set_new_working_dir()
                    case _:
                        add_to_terminal("cd: too many arguments")
            case "clear" | "c":
                if len(args) > 0:
                    add_to_terminal("clear: too many arguments")
                else:
                    terminal["text"] = ""
                    terminal.pack_forget()
                    global TERMINAL_HIDDEN
                    TERMINAL_HIDDEN = True
            case "vfs-save":
                match len(args):
                    case 0:
                        add_to_terminal("vfs-save needs and argument")
                    case 1:
                        if args[0].endswith(".json") or args[0].endswith(".txt"):
                            vfs.vfs_save(args[0])
                        else:
                            add_to_terminal(
                                "vfs-save path needs to end with a *.json or *.txt file"
                            )
                    case _:
                        add_to_terminal("vfs-save: too many arguments")
            case "vfs-load":
                match len(args):
                    case 0:
                        add_to_terminal("vfs-load needs and argument")
                    case 1:
                        if args[0].endswith(".json") or args[0].endswith(".txt"):
                            vfs.vfs_load(args[0])
                        else:
                            add_to_terminal(
                                "vfs-load path needs to end with a *.json or *.txt file"
                            )
                    case _:
                        add_to_terminal("vfs-load: too many arguments")
            case "tail":
                match len(args):
                    case 0:
                        add_to_terminal("tail needs an argument")
                    case 1:
                        add_to_terminal(vfs.tail(args[0]))
                    case _:
                        add_to_terminal("tail: too many arguments")
            case "rev":
                match len(args):
                    case 0:
                        add_to_terminal("rev needs an argument")
                    case 1:
                        add_to_terminal(vfs.rev(args[0]))
                    case _:
                        add_to_terminal("rev: too many arguments")
            case "wc":
                match len(args):
                    case 0:
                        add_to_terminal("wc needs an argument")
                    case 1:
                        add_to_terminal(vfs.wc(args[0]))
                    case _:
                        add_to_terminal("wc: too many arguments")
            case "cat":
                match len(args):
                    case 0:
                        add_to_terminal("cat needs an argument")
                    case 1:
                        add_to_terminal(vfs.cat(args[0]))
                    case _:
                        for arg in args:
                            add_to_terminal(vfs.cat(arg))
            case "chown":
                match len(args):
                    case 2:
                        add_to_terminal(vfs.chown(args[0], args[1]))
                    case _:
                        add_to_terminal(
                            f"chown takes exactly 2 arguments. provided: {len(args)}"
                        )
            case "rm":
                match len(args):
                    case 0:
                        add_to_terminal("rm needs an argument")
                    case 1:
                        add_to_terminal(vfs.rm(args[0]))
                    case _:
                        add_to_terminal("rm: too many arguments")
            case _:
                add_to_terminal(f"command not found: {command}")

    def handle_script():
    # Command implementation
        
        for command in get_startup_script():
            add_to_terminal(command, True)
            command, args = (parse_args(command))
            match command:
                case None:
                    pass
                case "exit":
                    root.destroy()
                case "ls":
                    match len(args):
                        case 0:
                            add_to_terminal(vfs.ls())
                        case 1:
                            add_to_terminal(vfs.ls(args[0]))
                        case _:
                            for arg in args:
                                add_to_terminal(f" {arg}:")
                                add_to_terminal(vfs.ls(arg))
                case "cd":
                    match len(args):
                        case 0:
                            add_to_terminal(vfs.cd())
                            set_new_working_dir()
                        case 1:
                            add_to_terminal(vfs.cd(args[0]))
                            set_new_working_dir()
                        case _:
                            add_to_terminal("cd: too many arguments")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                case "clear" | "c":
                    if len(args) > 0:
                        add_to_terminal("clear: too many arguments")
                        add_to_terminal("SCRIPT FAILED. TERMINATING")
                        break
                    else:
                        terminal["text"] = ""
                        terminal.pack_forget()
                        global TERMINAL_HIDDEN
                        TERMINAL_HIDDEN = True
                case "vfs-save":
                    match len(args):
                        case 0:
                            add_to_terminal("vfs-save needs and argument")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                        case 1:
                            if args[0].endswith(".json") or args[0].endswith(".txt"):
                                vfs.vfs_save(args[0])
                            else:
                                add_to_terminal(
                                    "vfs-save path needs to end with a *.json or *.txt file"
                                )
                                add_to_terminal("SCRIPT FAILED. TERMINATING")
                                break
                        case _:
                            add_to_terminal("vfs-save: too many arguments")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                case "vfs-load":
                    match len(args):
                        case 0:
                            add_to_terminal("vfs-load needs and argument")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                        case 1:
                            if args[0].endswith(".json") or args[0].endswith(".txt"):
                                vfs.vfs_load(args[0])
                            else:
                                add_to_terminal(
                                    "vfs-load path needs to end with a *.json or *.txt file"
                                )
                                add_to_terminal("SCRIPT FAILED. TERMINATING")
                                break
                        case _:
                            add_to_terminal("vfs-load: too many arguments")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                case "tail":
                    match len(args):
                        case 0:
                            add_to_terminal("tail needs an argument")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                        case 1:
                            add_to_terminal(vfs.tail(args[0]))
                        case _:
                            add_to_terminal("tail: too many arguments")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                case "rev":
                    match len(args):
                        case 0:
                            add_to_terminal("rev needs an argument")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                        case 1:
                            add_to_terminal(vfs.rev(args[0]))
                        case _:
                            add_to_terminal("rev: too many arguments")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                case "wc":
                    match len(args):
                        case 0:
                            add_to_terminal("wc needs an argument")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                        case 1:
                            add_to_terminal(vfs.wc(args[0]))
                        case _:
                            add_to_terminal("wc: too many arguments")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                case "cat":
                    match len(args):
                        case 0:
                            add_to_terminal("cat needs an argument")
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                        case 1:
                            add_to_terminal(vfs.cat(args[0]))
                        case _:
                            for arg in args:
                                add_to_terminal(vfs.cat(arg))
                case "chown":
                    match len(args):
                        case 2:
                            add_to_terminal(vfs.chown(args[0], args[1]))
                        case _:
                            add_to_terminal(
                                f"chown takes exactly 2 arguments. provided: {len(args)}"
                            )
                            add_to_terminal("SCRIPT FAILED. TERMINATING")
                            break
                case "unterminated_comma_mistake\1\2":
                    add_to_terminal("SCRIPT FAILED. TERMINATING")
                    break
                case "rm":
                    match len(args):
                        case 0:
                            add_to_terminal("rm needs an argument")
                            break
                        case 1:
                            add_to_terminal(vfs.rm(args[0]))
                        case _:
                            add_to_terminal("rm: too many arguments")
                            break
                case _:
                    add_to_terminal(f"command not found: {command}")
                    break

    def handleExecuteButton(event=None):
        unhide_terminal()
        add_to_terminal(input_field.get(), True)
        handle_args(parse_args())
        input_field.delete(0, "end")
        input_field.focus()

    
    root.bind("<Return>", handleExecuteButton)

    execute_button = tk.Button(
        command=handleExecuteButton,
        borderwidth=0,
        highlightthickness=2,
        highlightbackground="#676464",
        highlightcolor="#676464",
        activebackground="#3B3B3B",
        activeforeground="#000000",
        background="#1C1C1C",
        foreground="#616365",
        text="Execute",
    ).pack(side="right", anchor=tk.SE)

    def handleClearButton(event=None):
        handle_args(("clear", []))

    clear_button = tk.Button(
        command=handleClearButton,
        borderwidth=0,
        highlightthickness=2,
        highlightbackground="#676464",
        highlightcolor="#676464",
        activebackground="#3B3B3B",
        activeforeground="#000000",
        background="#1C1C1C",
        foreground="#616365",
        text="Clear",
    ).pack(side="bottom", anchor=tk.SE)

    container.pack(side="top")
    prefix.pack(in_=container, side="left")
    input_field.pack(in_=container, side="left")
    input_field.focus()

    
    if get_startup_script():
        handle_script()
    unhide_terminal()
    set_new_working_dir()

    root.mainloop()


if __name__ == "__main__":
    vfs = Vfs(PATHS["VFS"])
    gui()
