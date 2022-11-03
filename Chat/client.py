#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cliente de Chat
* Autor(es): Michel Paola Osornio Torres, Guennadi Maximov Cortés
* Última Edición: 03-11-2022
"""
import socket as sock
import sys
from time import sleep

HOST = '127.0.0.1'
ENC = 'utf-8'


def b(*words, sep=' ', enc=ENC) -> bytes:
    """Convierte una o muchas cadenas a un objeto `bytes` ya codificado."""
    w_s = sep.join(words)
    return bytes(w_s, encoding=enc)


def main(port: int) -> int:
    """Función principal"""
    ret = 0

    sck = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    sck.connect((HOST, port))
    sleep(5)

    try:
        msg = sck.recv(1024)
        print(msg.decode(ENC))
        sck.send(bytes("Client: Thank you, I'm your client number 1",
                       encoding=ENC))

        msg1 = sck.recv(1024)
        print(msg1.decode(ENC))

    except KeyboardInterrupt:
        ret = -1
        print('ABORTING...',
              file=sys.stderr)

        sck.close()
        sleep(3)

    except Exception:
        ret = 1
        print("SOMETHING WENT WRONG...",
              file=sys.stderr)

        sck.close()
        sleep(3)

    sck.close()

    return ret


if __name__ == '__main__':
    port = 0

    while port <= 0:
        try:
            print('Seleccione el puerto:', end=' ')
            port = int(input().strip().lstrip('0'))

        except KeyboardInterrupt:
            print('ABORTING...',
                  file=sys.stderr)

            sleep(3)
            sys.exit(-1)

        except ValueError:
            print(f'Invalid Port value "{port}"',
                  file=sys.stderr)

            sleep(3)
            continue

        except Exception:
            print('Something went wrong. Try again...',
                  file=sys.stderr)

            sleep(3)
            continue

    sys.exit(main(port))
