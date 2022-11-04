#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor de Chat.
* Autor(es): Michel Paola Osornio Torres, Guennadi Maximov Cortés
* Última Edición: 02-11-2022
"""
import socket as sock
import sys
# import threading as thr
from time import sleep
from typing import List, NoReturn, Tuple

HOST = '127.0.0.1'
PORT = 6060
ENC = 'utf-8'
BUF_S = 1024
MAX_CLIENTS = 10


def b(*words, sep=' ', enc=ENC) -> bytes:
    """Convierte una o muchas cadenas a un objeto `bytes` ya codificado."""
    return bytes(sep.join(words), encoding=enc)


class Server:
    """Server class."""

    def __init__(self,
                 host: str,
                 port: int,
                 str_id='SERVER',
                 logf=('./server_history', 'a')):
        """Método Constructor."""
        self.hp_tup = (host, port)
        self.host, self.port = self.hp_tup
        self.id = str_id

        self.binded = False
        self.listening = False

        self.all_clients = set()
        self.active_clients = set()
        self.taken_addr = set()
        self.taken_nicks = set()

        self.start()

    def _start_cond(self) -> List[bool, bool]:
        return [self.binded, self.listening]

    def start(self) -> NoReturn:
        """Inicializa el servidor con los sockets."""
        if self._start_cond() == [False, False]:
            self.sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            self.sock.bind(self.hp_tup)
            self.binded = True
            self.sock.listen()
            self.listening = True

    def accept(self):
        """Acepta un socket."""
        client, addr = self.sock.accept()
        is_new = True
        req_nick = True

        for d in self.all_clients:
            if client == d.get('csock') and addr == d.get('addr'):
                is_new = False

                if d.get('nick', False):
                    req_nick = False

                break

        if is_new and req_nick:
            avail_nick = False
            omsg = 'Welcome! Please input your nickname: '
            while not avail_nick:
                client.send(b(omsg))

                nick = client.recv(BUF_S).decode(ENC)
                # TODO: Add Validator, import string module
                if len(self.taken_nicks) == 0:
                    avail_nick = True
                    self.taken_nicks.add(nick)

                elif nick not in self.taken_nicks:
                    avail_nick = True
                    self.taken_nicks.add(nick)

                else:
                    omsg = f'Username {nick} is already taken. Please try again: '
                    continue

    def close(self, t=30) -> NoReturn:
        if t in [int, float]:
            t = abs(int(t))

            if t == 0 or t >= 1800:
                t = 30

        elif t not in [int]:
            t = 30

        for c in self.active_clients:
            c.send(b("[{SERVIDOR}]: El servidor se cerrará en {t} segundos."))

        sleep(t)

        for c in self.active_clients:
            c.close()

        self.sock.close()
        self.binded = False
        self.listening = False


def main(port: int) -> int:
    """Función principal."""
    srv = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    srv.bind((HOST, port))
    srv.listen()

    imsg, omsg, all_omsg = list(), list(), list()
    n_cli = 1

    while n_cli <= MAX_CLIENTS:
        client, address = srv.accept()
        nick = f'user{n_cli}@{address}'
        print("Connection is established:",
              f'"{nick}"')

        omsg.append(f'Server: "{nick}@{address}", you are connected.')
        client.send(b(omsg[-1]))

        imsg.append(client.recv(BUF_S).decode(ENC))
        print(imsg[-1])

        # for i in range(9, 1, -1):
        #     print(i)

        omsg.append("Logging you off. Bye!")
        client.send(b(omsg[-1]))

        client.close()

    srv.sendall(b("Server shutting down in 5 seconds.\nBye!"))
    srv.close()
    return 0


if __name__ == '__main__':
    sys.exit(main(PORT))
