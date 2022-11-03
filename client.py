#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cliente de Chat
* Autor(es): Michel Paola Osornio Torres, Guennadi Maximov Cortés
* Última Edición: 02-11-2022
"""
import socket as sock
import sys
from time import sleep

HOST = '127.0.0.1'
ENC = 'utf-8'


def main(PORT: int) -> int:
    """Función principal"""
    ret = 0

    sck = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    sck.connect((HOST, PORT))
    sleep(5)

    try:
        msg = sck.recv(1024)
        print(msg.decode(ENC))
        sck.send(bytes("Client: Thank you, I'm your client number 1",
                       encoding=ENC))

        msg1 = sck.recv(1024)
        print(msg1.decode(ENC))

        sck.close()

    except KeyboardInterrupt:
        ret = -1
        print('ABORTING . . .',
              file=sys.stderr)

        sck.close()
        sleep(3)

    except Exception:
        ret = 1
        print("SOMETHING WENT WRONG...",
              file=sys.stderr)

        sck.close()
        sleep(3)

    return ret


if __name__ == '__main__':
    PORT = 0

    while PORT <= 0:
        try:
            PORT = int(input("Select port: ").strip().lstrip('0'))

            if PORT <= 0:
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

    sys.exit(main(PORT))
