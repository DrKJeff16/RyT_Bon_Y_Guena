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
BUF_S = 1024


def b(*words, sep=' ', enc=ENC) -> bytes:
    """Convierte una o muchas cadenas a un objeto `bytes` ya codificado."""
    return bytes(sep.join(words), encoding=enc)


def main(port_n: int) -> int:
    """Función principal"""
    sck = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    sck.connect((HOST, port_n))
    sleep(3)
    imsg, omsg = list(), list()

    imsg.append(sck.recv(BUF_S).decode(ENC))
    print(imsg[-1])

    sleep(1)

    omsg.append("Client: Thank you, I'm your client number 1")
    sck.send(b(omsg[-1]))
    sleep(1)

    imsg.append(sck.recv(BUF_S).decode())
    print(imsg[-1])

    sck.close()
    return 0


if __name__ == '__main__':
    port_n = 0

    while port_n <= 0:
        try:
            print('Seleccione el puerto:', end=' ')
            port_n = int(input().strip().lstrip('0'))

        except KeyboardInterrupt:
            print('ABORTING...',
                  end='\n\n',
                  file=sys.stderr)
            sleep(2)
            sys.exit(-1)

        except ValueError:
            print(f'Invalid Port value "{port_n}".',
                  'Try again.',
                  sep='\n',
                  end='\n\n',
                  file=sys.stderr)
            sleep(2)
            continue

        except Exception:
            print('Something went wrong.',
                  'Try again.',
                  sep='\n',
                  end='\n\n',
                  file=sys.stderr)
            sleep(2)
            continue

    sys.exit(main(port_n))
