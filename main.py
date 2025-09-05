import tkinter as tk
from tkinter import ttk
import json
import os, platform, sys, socket
import argv_handling
import VFS as p

LOGIN = os.getlogin()
HOSTNAME = socket.gethostname()
CURRENT_SYSTEM = platform.system()
TERMINAL_HIDDEN = True

PATHS = argv_handling.handle_args()


def get_startup_script():
    path = PATHS["script"]
    if path:
        with open(path, 'r') as suf:
            return [x.removesuffix('\n') for x in suf]
    else: 
        return []

   
def gui():
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 512
    global TERMINAL_HIDDEN
    
    if CURRENT_SYSTEM == "Linux":
        FONT = "Modern"
        PREFIX_WIDTH = len(f"{LOGIN}@{HOSTNAME}$") + 1
    else:
        FONT = "Arial"
        PREFIX_WIDTH = len(f"{LOGIN}@{HOSTNAME}$")
    
    root = tk.Tk()
    
    if root:
        root.configure(background="black", padx=3, pady=4),
        root.title(f"{LOGIN}@{HOSTNAME}")
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
    container = tk.Frame(highlightthickness=0,
                         borderwidth=0,
                         pady=0,
                         background="red")
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
        width=int(WINDOW_WIDTH * 0.75),
    )
    prefix = tk.Label(container,
                      borderwidth=0,
                      width=PREFIX_WIDTH,
                      padx=0,
                      anchor="nw",
                      background="black",
                      justify="left",
                      foreground="lime",
                      font=FONT,
                      text=f"{LOGIN}@{HOSTNAME}$")

    def unhide_terminal():
        global TERMINAL_HIDDEN
        if TERMINAL_HIDDEN:
            TERMINAL_HIDDEN = False
            container.pack_forget()

            terminal.pack(side="top", )

            container.pack(side="top", )

            prefix.pack(in_=container, side="left")
            input_field.pack(
                in_=container,
                side="left",
            )

    def add_to_terminal(inp, with_login=False):
        if with_login:
            if terminal["text"] == "":
                terminal["text"] += f"{LOGIN}@{HOSTNAME}$ {inp}"
            else:
                terminal["text"] += f"\n{LOGIN}@{HOSTNAME}$ {inp}"
        else:
            terminal["text"] += f"\n{inp}"
            
    def parse_args(inp=None):
        if not inp:
            inp=input_field.get().replace("'", '"')
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
                raise Exception("Unterminated comma")
            # in case command is made of several words, i.e. 'good cd' should be a command {good cd}
            if comma_args and (command in comma_args[0]):
                command = comma_args[0].removeprefix('"').removesuffix('"')
                print(command)
            elif comma_args:
                args.append(comma_args[0].removeprefix('"').removesuffix('"'))
                inp = inp.replace(comma_args[0], "")

            for arg in comma_args[1:]:
                args.append(arg.removeprefix('"').removesuffix('"'))
                inp = inp.replace(arg, "")
            args += inp.split()[1:]
        except Exception as e:
            command = ""
            print('Error occured:', e)
        return (command or None, args or [])

    def handle_args(command_args):
        # Command implementation
        command, args = command_args
        match command:
            case None:
                print('No command provided')
            case "exit":
                root.destroy()
            case "ls":
                add_to_terminal("ls\targs: " + ", ".join(args))
            case "cd":
                if len(args) > 1:
                    add_to_terminal("cd: too many arguments")
                else:
                   add_to_terminal("cd\targs:" + ", ".join(args))

            case "clear":
                if len(args) > 0:
                    add_to_terminal("clear: too many arguments")
                else:
                    terminal["text"] = ""
                    terminal.pack_forget()
                    global TERMINAL_HIDDEN
                    TERMINAL_HIDDEN = True
            case _:
                add_to_terminal(f"command not found: {command}")

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
    ).pack(side="right", anchor=tk.NE)

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
    ).pack(side="top", anchor=tk.NE)

    container.pack(side="top", )
    prefix.pack(in_=container, side="left")
    input_field.pack(in_=container, side="left")
    input_field.focus()
    
    if get_startup_script():
        for command in get_startup_script():
            add_to_terminal(command, True)
            handle_args(parse_args(command))
        else: 
            unhide_terminal()
    root.mainloop()


if __name__ == '__main__':
    VFS = p.VFS(PATHS["VFS"])
    print(VFS.vfs)
    for x in VFS.vfs['root'].keys():
        print(x)
    gui()