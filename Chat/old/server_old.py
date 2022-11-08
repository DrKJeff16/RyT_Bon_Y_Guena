#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor de Chat.
* Autor(es): Michel Paola Osornio Torres, Guennadi Maximov Cortés
* Última Edición: 02-11-2022
"""
import random as rnd
import socket as sock
from string import punctuation as pnc
import sys
# import threading as thr
from time import sleep
from typing import Dict, List, NoReturn, Set, Tuple

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
    host: str
    port: int
    s_id: str
    binded: bool
    listening: bool
    all_clients: Dict[Tuple[str, int]: Dict[str: bool, str: str]]
    srv: sock.socket
    # active_clients: Set[Tuple[sock.socket, Tuple[str, int]]]
    # taken_addr: Dict
    # taken_nicks: Dict

    def __init__(self,
                 host: str,
                 port: int,
                 s_id='SERVER'):
        """Método Constructor."""
        self.host = host
        self.port = port
        self.s_id = s_id

        self.binded = False
        self.listening = False

        self.all_clients = dict()
        self.srv = None

        self.start()

    def addr(self) -> Tuple[str, int]:
        """Retorna la tupla host-puerto"""
        return self.host, self.port

    def start(self) -> NoReturn:
        """Inicializa el servidor con los sockets."""
        if not self.binded:
            self.srv = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            self.srv.bind(self.addr())
            self.binded = True

    def accept(self):
        """Acepta un socket."""
        if not self.listening:
            self.listening = True
            self.srv.listen()
            client, addr = self.srv.accept()
            self.listening = False

            cli_dict = self.all_clients.get((client, addr), None)

            if cli_dict is None:
                cli_dict = {(client, addr): {
                    'online': True
                }}
            else:
                cli_dict[(client, addr)].update({'online': True})

            if cli_dict[(client, addr)].get('nick', None) is None:
                try:
                    cli_dict[(client, addr)].update({
                        'nick': self.ask_nick((client, addr))
                    })
                except ConnectionError:
                    cli_dict[(client, addr)]['online'] = False
                    cli_dict[(client, addr)].update({
                        'nick': None
                    })
                except ConnectionResetError:
                    cli_dict[(client, addr)]['online'] = False
                    cli_dict[(client, addr)].update({
                        'nick': None
                    })
                except ConnectionAbortedError:
                    cli_dict[(client, addr)]['online'] = False
                    cli_dict[(client, addr)].update({
                        'nick': None
                    })
                except ConnectionRefusedError:
                    cli_dict[(client, addr)]['online'] = False
                    cli_dict[(client, addr)].update({
                        'nick': None
                    })
                except KeyboardInterrupt:
                    self.close(1)
                    sys.exit(-1)

    def ask_nick(self, c_a: Tuple[sock.socket, Tuple[str, int]]) -> str:
        """Pide al usuario su nickname."""
        cli = c_a[0]

        prompt = 'Bienvenido, usuario!', 'Ingrese su nickname.'
        while True:
            print(*prompt, sep='\n', end='\n\n')
            cli.send(b(prompt[0]))
            cli.send(b(prompt[1]))
            nick = cli.recv(BUF_S).decode(ENC).strip()

            cond = (
                    len(nick) == 0,
                    nick.isascii(),
                    any([c in ''.join(
                        [p for p in pnc if p not in '._-'] + ' \t\r\n')
                         for c in nick]))

            if not all(cond):
                prompt = 'INVALID', 'Vuelva a intentarlo.'
                cli.send(b(prompt[0]))
                cli.send(b(prompt[1]))
            else:
                prompt = 'VALID', f'Bienvenido/a, {nick}'
                cli.send(b(prompt[0]))
                cli.send(b(prompt[1]))
                return nick

    def close(self, t=10) -> NoReturn:
        active_clients = set()

        for c_a, attrs in zip(self.all_clients.keys(), self.all_clients.values()):
            if attrs.get('online'):
                c = c_a[0]
                c.send(b(f'[{self.s_id}]: Cierre del servidor en {t} segundos...'))
                active_clients.add(c)

        sleep(t)

        for c in active_clients:
            c.close()

        self.srv.close()
        self.binded = False


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
