#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor de Chat.
* Autor(es): Michel Paola Osornio Torres, Guennadi Maximov Cortés
* Última Edición: 02-11-2022
"""
import socket as sock
import sys
import threading as thr
from time import sleep

HOST = '127.0.0.1'
ENC = 'utf-8'


def main(port: int) -> int:
    """Función principal."""
    ret = 0

    srv = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    srv.bind((HOST, port))
    srv.listen(1)

    try:
        while True:
            csocket, address = srv.accept()
            print("Connection is stablished: ", address)
            csocket.send(bytes("Server: You are connected",
                               encoding=ENC))
            msg = csocket.recv(1024)
            print(msg.decode(ENC))
            sleep(12)
            csocket.send(bytes("bye"))
            csocket.close()

        srv.close()
    except KeyboardInterrupt:
        ret = -1
        print("ABORTING . . .",
              file=sys.stderr)

        srv.close()
        sleep(3)

    except Exception:
        ret = 1
        print("SOMETHING WENT WRONG...",
              file=sys.stderr)

        srv.close()
        sleep(3)

    return ret


if __name__ == '__main__':
    port = 0

    while port <= 0:
        try:
            port = int(input("Select port: ").strip().lstrip('0'))

            if port <= 0:
                raise ValueError("")

        except KeyboardInterrupt:
            print('ABORTING . . .',
                  file=sys.stderr)

            sleep(3)
            sys.exit(-1)

        except ValueError:
            print('Invalid Port value, cannot be less than 1!',
                  file=sys.stderr)

            sleep(3)
            continue

        except Exception:
            print('Something went wrong. Try again...',
                  file=sys.stderr)

            sleep(3)
            continue

    sys.exit(main(port))
