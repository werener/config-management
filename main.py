import tkinter as tk
from tkinter import ttk
import os
import socket

LOGIN = os.getlogin()
HOSTNAME = socket.gethostname()

WINDOW_WIDTH = 512
WINDOW_HEIGHT = 256

TERMINAL_HIDDEN = True

root = tk.Tk()
root.configure(background='blue')
root.title(f'{LOGIN}@{HOSTNAME}')
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

container = tk.Frame(borderwidth=0, pady=0,background='red')
terminal = ttk.Label(text='',
                     background='black',
                     borderwidth=0,
                     width=WINDOW_WIDTH,
                     foreground='white')

input_field = tk.Entry(container,
                       background='black',
                       foreground='white',
                       borderwidth=0,
                       width=int(WINDOW_WIDTH * 0.75))
prefix = tk.Label(container,
                  width=14,
                  padx=2,
                  background='black',
                  foreground='white')

prefix['text'] = f'{LOGIN}@{HOSTNAME}$ '


def handleExecuteButton(event=None):

    def add_to_terminal():
        inp = input_field.get()
        if terminal['text'] == '':
            terminal['text'] += f'{LOGIN}@{HOSTNAME}$ {inp}'
        else:
            terminal['text'] += f'\n{LOGIN}@{HOSTNAME}$ {inp}'

    def handle_args():
        inp = input_field.get().split()
        args = inp[1:]
        command = inp[0]
        match command:
            case 'exit':
                root.destroy()
            case 'ls':
                terminal['text'] += '\nls ' + ' '.join(args)

    add_to_terminal()
    handle_args()
    global TERMINAL_HIDDEN
    if TERMINAL_HIDDEN:
        TERMINAL_HIDDEN = False
        terminal.pack(anchor=tk.NW)
    input_field.delete(0, 'end')


root.bind('<Return>', handleExecuteButton)

execute_button = ttk.Button(command=handleExecuteButton,
                            text='Execute command').pack(side='top',anchor=tk.NE)

terminal.pack(side='top', padx=0)

container.pack(side='top')

prefix.pack(in_=container, side="left")
input_field.pack(in_=container, side='left')

input_field.focus()

root.mainloop()
