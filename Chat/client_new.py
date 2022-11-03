#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GUI client from tutorial"""
from collections import deque as dq
import os
import sys
import string as s
import socket as sock
import threading as thr
from typing import AnyStr, Set, NoReturn, Tuple
import tkinter as tk
import tkinter.simpledialog as sd

HOST = '127.0.0.1'
ENC = 'utf-8'
BUF_S = 1024


def b(*st, enc=ENC, sep=' ') -> bytes:
    """Return an encoded bytes object."""
    return bytes(sep.join(st), encoding=enc)


class Client:
    """Client-type object."""

    def __init__(self,
                 host: str,
                 port: int):
        """Constructor Method."""
        # av_keys = {
        #        'history': {
        #            'default': True,
        #            'type': 'bool',
        #            'values': {
        #                (None, False, 0, 0.): False
        #            }
        #        },
        #        'histsize': {
        #            'default': 100,
        #            'type': 'range',
        #            'max': 5000,
        #            'min': 1
        #        },
        #        'histfile': {
        #            'default': './.history',
        #            'type': 'file',
        #            'depends_on': 'history'
        #        },
        #        'padx_all': {
        #            'default': 25,
        #            'type': 'range',
        #            'max': 100,
        #            'min': 0,
        #        },
        #        'pady_all': {
        #            'default': 5,
        #            'type': 'range',
        #            'max': 20,
        #            'min': 0
        #        }
        # }

        # k_types = {
        #    'range': ''
        # }

        # processed_keys = set()

        # for k, v in kwargs.items():
        #    if k not in av_keys.keys():
        #        raise KeyError(f'Option "{k}" not found')

        #    if k not in processed_keys:
        #        processed_keys.add(k)
        #        instructions = av_keys.get(k)

        #        if None not in [instructions.get(a, None)
        #            for a in ['min', 'max']] and 'range' 
        #        == instructions.get('type'):
        #            if v in instructions.get('except', list()):
        #                raise ValueError(f'Invalid value "{v}"')

        #            allowed = range(instructions.get('min'),
        #                            instructions.get('max') + 1)

        #            if v not in allowed:
        #                raise ValueError(f'Invalid value "{v}"')

        self.h_p = tuple(host, port)
        self.connected = False
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.connect()

        msg = tk.Tk()
        msg.withdraw()

        self.nick = sd.askstring("Nickname",
                                 "Please Choose a Nickname",
                                 parent=msg)

        self.gui_done = False
        self.running = True

        self.msg_history

        gui_thread = thr.Thread(target=self.gui_loop)
        recv_thread = thr.Thread(target=self.receive)

        gui_thread.start()
        recv_thread.start()

    def connect(self) -> NoReturn:
        """Connect the socket."""
        if not self.connected:
            self.sock.connect(self.h_p)
            self.connected = True
        else:
            print('[WARNING]:\n\t',
                  f'Connection to Socket "{self.sock} is already"',
                  'established.',
                  file=sys.stderr)

    def gui_loop(self):
        """GUI Looping."""
        self.win = tk.Tk()
        self.win.configure(bg='darkblue')

        self.chat_label = tk.Label(self.win, text='Chat:', bg='darkblue')
        self.chat_label.configure(font=('Arial', 15))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tk.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.configure(state='disabled')

        self.msg_label = tk.Label(self.win, text='Message:', bg='darkblue')
        self.msg_label.configure(font=('Arial', 15))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self.win, height=5)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self.win, text='Send', command=self.write)
        self.send_button.configure(font=('Arial', 15))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol('WM_DELETE_WINDOW', self.stop)
        self.win.mainloop()

    def write(self):
        """Writer function."""
        msg

    def stop(self):
        """Stopper function."""
        if self.gui_done and self.running:
            self.running = False
            self.win.destroy()
            self.sock.close()

            sys.exit(0)

    def receive(self):
        """Instance Receiver."""
        pass


def main(port_n: int) -> int:
    """Main function."""
    ret = 0

    if port_n <= 0:
        ret = -1

    return ret


if __name__ == '__main__':
    port_n = input("Select Port: ").strip()
    sys.exit(main(port_n))
