#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cliente de Chat
* Autor(es): Michel Paola Osornio Torres, Guennadi Maximov Cortés
* Última Edición: 03-11-2022
"""
# from collections import deque as dq
import socket as sock
import sys
from time import sleep

HOST = '127.0.0.1'
ENC = 'utf-8'
BUF_S = 1024


def b(*words, sep=' ', enc=ENC) -> bytes:
    """Convierte una o muchas cadenas a un objeto `bytes` ya codificado."""
    return bytes(sep.join(words), encoding=enc)


def main(port: int) -> int:
    """Función principal"""
    sck = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    sck.connect((HOST, port))
    sleep(3)

    imsg = list()
    omsg = list()
    cl_n = 0

    while cl_n < 10:
        try:
            cl_n += 1
            imsg.append(sck.recv(BUF_S).decode(ENC))
            print(imsg[-1])
            sleep(6)

            omsg.append("Client: Thank you, I'm your client number 1")
            sck.send(b(omsg[-1]))

            imsg.append(sck.recv(BUF_S).decode(ENC))
            print(imsg[-1])

        except KeyboardInterrupt:
            sck.send(b("I'm leaving, bye!"))
            sleep(2)
            sck.close()
            return -1

        except Exception:
            print("SOMETHING WENT WRONG...",
                  'Disconnecting.',
                  sep='\n',
                  file=sys.stderr)
            sck.send(b("I'm leaving for an unknown reason :("))
            sleep(3)
            sck.close()
            return 2

    return 0


if __name__ == '__main__':
    port_n = 0

    while port_n <= 0:
        print('Seleccione el puerto:',
              end=' ')
        port_n = int(input().strip().lstrip('0'))

    sys.exit(main(port_n))
