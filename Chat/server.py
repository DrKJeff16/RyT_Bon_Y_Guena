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

HOST = '127.0.0.1'
ENC = 'utf-8'


def b(*words, sep=' ', enc=ENC) -> bytes:
    """Convierte una o muchas cadenas a un objeto `bytes` ya codificado."""
    w_s = sep.join(words)
    return bytes(w_s, encoding=enc)


def main(port: int) -> int:
    """Función principal."""
    ret = 0

    srv = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    srv.bind((HOST, port))
    srv.listen()

    try:
        while True:
            try:
                csocket, address = srv.accept()
                print("Connection is established:", address)

                omsg = b("Server: You are connected.")
                csocket.send(omsg)

                imsg = csocket.recv(1024)
                print(imsg.decode(ENC))
                sleep(12)
                omsg = b("Bye!")
                csocket.send(omsg)

            except Exception:
                ret = 2

            finally:
                csocket.close()

    except KeyboardInterrupt:
        csocket.close()
        ret = -1
        print("ABORTING...",
              file=sys.stderr)
        sleep(3)

    except Exception:
        ret = 2
        print("SOMETHING WENT WRONG...",
              file=sys.stderr)
        sleep(3)

    finally:
        srv.close()
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
