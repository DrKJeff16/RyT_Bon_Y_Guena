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

    def __init__(self, host: str, port: int, str_id='SERVER', backlog=None):
        """Método Constructor."""
        self.hp_tup = (host, port)
        self.host, self.port = self.hp_tup
        self.id = str_id

        self.backlog = backlog

        self.binded = False
        self.listening = False

        self.all_clients = set()
        self.active_clients = set()

        self.start()

    def _start_cond(self) -> List[bool, bool]:
        return [self.binded, self.listening]

    def start(self) -> NoReturn:
        """Inicializa el servidor con los sockets."""
        if self._start_cond() == [False, False]:
            self.sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            self.sock.bind(self.hp_tup)
            self.binded = True

            self.listen()

        elif self._start_cond() == [True, True]:
            pass

        elif self._start_cond() == [True, False]:
            self.listen()

    def listen(self) -> NoReturn:
        """Start Listening"""
        if self._start_cond() == [True, False]:
            if self.backlog is None:
                self.sock.listen()
            else:
                self.sock.listen(self.backlog)

            self.listening = True

        elif self._start_cond() == [True, True]:
            pass

        elif self._start_cond() == [False, False]:
            self.start()

        else:
            sys.exit(1)

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


class Client:
    """Client class."""

    def __init__(self, srv: sock.socket):
        """Constructor Method."""
        self.sock, self.addr = srv.accept()
        self.connected = True

        self.imsg = list()
        self.omsg = list()

    def serv_send(self, *args: Tuple[str]) -> NoReturn:
        """Send a message to client from server."""
        pass


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
