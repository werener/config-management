import tkinter as tk
from tkinter import ttk
import os
import socket
import re

LOGIN = os.getlogin()
HOSTNAME = socket.gethostname()

WINDOW_WIDTH = 512
WINDOW_HEIGHT = 256

TERMINAL_HIDDEN = True

root = tk.Tk()
root.configure(background='black', padx=3, pady=4)
root.title(f'{LOGIN}@{HOSTNAME}')
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

container = tk.Frame(borderwidth=0, pady=0, background='red')
terminal_text = ''
terminal = tk.Label(text='',
                    pady=0,
                    padx=0,
                    anchor='nw',
                    background='black',
                    justify='left',
                    borderwidth=0,
                    width=WINDOW_WIDTH,
                    foreground='white')

input_field = tk.Entry(
    container,
    #    cursor='green',
    justify='left',
    background='black',
    foreground='white',
    borderwidth=0,
    selectbackground='white',
    selectforeground='black',
    insertbackground='white',
    insertborderwidth=2,
    insertwidth=3,
    insertofftime=0,
    width=int(WINDOW_WIDTH * 0.75))
prefix = tk.Label(container,
                  borderwidth=0,
                  width=15,
                  padx=0,
                  anchor='nw',
                  background='black',
                  justify='left',
                  foreground='lime')

prefix['text'] = f'{LOGIN}@{HOSTNAME}$'


def handleExecuteButton(event=None):

    def add_to_terminal():
        inp = input_field.get()
        if terminal['text'] == '':
            terminal['text'] += f'{LOGIN}@{HOSTNAME}$  {inp}'
        else:
            terminal['text'] += f'\n{LOGIN}@{HOSTNAME}$  {inp}'

    def handle_args():
        # try:
            inp = input_field.get().split()
            
            command = inp[0]

            def map_input(inp):
                parameters, args = [], []
                for arg in inp:
                    if re.fullmatch(r"[\'\"].{0,}[\'\"]", arg):
                        parameters.append(arg)
                    else:
                        args.append(arg)
                return parameters, args
            
            parameters, args = map_input(inp[1:])

            match command:
                case 'exit':
                    root.destroy()
                case 'ls':
                    terminal['text'] += '\nls  args: ' + ' '.join(args) + '  parameters: ' + ' '.join(parameters)
                case 'cd':
                    terminal['text'] += '\ncd  args:' + ' '.join(args) + '  parameters' + ' '.join(parameters)
                case _:
                    terminal['text'] += f'\ncommand not found: {command}'

        # except:
        #     print('no input given')

    add_to_terminal()
    handle_args()
    global TERMINAL_HIDDEN
    if TERMINAL_HIDDEN:
        TERMINAL_HIDDEN = False
        container.pack_forget()

        terminal.pack(side='top', )

        container.pack(side='top', )

        prefix.pack(in_=container, side="left")
        input_field.pack(
            in_=container,
            side='left',
        )

        input_field.focus()
    input_field.delete(0, 'end')
    input_field.focus()


root.bind('<Return>', handleExecuteButton)

execute_button = tk.Button(command=handleExecuteButton,
                           borderwidth=0,
                           background="#1C1C1C",
                           foreground="#616365",
                           text='Execute')
execute_button.pack(side='top', anchor=tk.NE)

# terminal.pack(side='top', )

container.pack(side='top', )

prefix.pack(in_=container, side="left")
input_field.pack(
    in_=container,
    side='left',
)

input_field.focus()

root.mainloop()
