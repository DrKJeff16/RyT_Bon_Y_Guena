#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor de Caht."""
import random as rnd
import socket as sock
import string as s
import sys
import threading as thr
from time import sleep
from typing import NoReturn, Set, Tuple

HOST = '127.0.0.1'
ENC = 'utf-8'
BUF_S = 1024
MAX_TRIES = 5


def b(*st, enc=ENC, sep=' ') -> bytes:
    """Convert to encoded bytes"""
    return bytes(sep.join(st), encoding=ENC)


def validate_nick(n_s: str) -> Tuple[bool, str]:
    """Validate a nickname."""
    u = ''.join([c for c in s.punctuation if c not in '_.-'])
    u += '\n\t\r'

    r_dict = {
        '0': 'Nickname is empty',
        '1': 'Nickname contains spaces.',
        '2': 'Nickname contains non-ASCII characters',
        '3': f'Nickname has one of these invalid characters: "{u}"'
    }

    if len(n_s) == 0:
        return False, r_dict.get('0')
    if ' ' in n_s:
        return False, r_dict.get('1')
    if not n_s.isascii():
        return False, r_dict.get('2')
    for c_h in n_s:
        if c_h in u:
            return False, r_dict.get('3')

    return True, 'NONE'


def broadcast(c_s: Set[sock.socket], msg: bytes) -> NoReturn:
    """Broadcast a Message To Everyone."""
    for c_h in c_s:
        c_h.send(msg)


def handle(client: sock.socket,
           n_s: Set[bytes],
           c_s: Set[sock.socket]) -> NoReturn:
    """Handler Function."""
    idx = list(c_s).index(client)
    nick = n_s[idx]

    while True:
        try:
            omsg = client.recv(BUF_S)
            print(f'[{nick}]: "{omsg}"')
            broadcast(c_s, omsg)

        except Exception:
            c_s.remove(client)
            client.close()
            n_s.remove(nick)

            break


def receive(srv: sock.socket,
            c_s: Set[sock.socket],
            n_s: Set[bytes]) -> NoReturn:
    """Recieve Message"""
    while True:
        nick = ''
        nick2 = b(nick)
        invalid_nick = True
        tries = 1
        client, addr = srv.accept()

        for i in range(rnd.randint(3, 8)):
            sleep(rnd.randint(1, 2))
            print('.', end='')

        sleep(2)
        print(f'Connection established with \'{str(addr)}\'',
              end='\n\n')
        sleep(3)

        try:
            while invalid_nick and tries < MAX_TRIES:
                try:
                    print('Insert your nickname: ', end='')
                    nick = input().strip()
                    validated, reason = validate_nick(nick)

                    if not validated:
                        if tries >= MAX_TRIES:
                            print('You have exceeded the amount of tries.',
                                  'Aborting...',
                                  sep='\n',
                                  end='\n\n',
                                  file=sys.stderr)
                            srv.close()
                            sleep(3)
                            sys.exit(2)

                        else:
                            print(f'Invalid nickname!\n\tReason: "{reason}"',
                                  f'You have {MAX_TRIES - tries} tries left',
                                  sep='\n',
                                  file=sys.stderr)
                            sleep(2)
                            print('Try again...',
                                  end='\n\n',
                                  file=sys.stderr)
                            sleep(2)
                            continue

                except KeyboardInterrupt:
                    sleep(2)
                    srv.close()
                    sys.exit(-1)

                except Exception:
                    print('SOMETHING WENT WRONG',
                          'ABORTING...',
                          sep='\n',
                          end='\n\n',
                          file=sys.stderr)
                    sleep(3)
                    srv.close()
                    sys.exit(2)

                finally:
                    tries += 1
                    sleep(2)
                    continue

        except KeyboardInterrupt:
            sleep(2)
            srv.close()
            sys.exit(-1)

        if len(nick) == 0:
            nick = f'Username{rnd.choice(["", ".", "_", "-"])}'
            nick += '{rnd.randint(1, 60000)}'

            while b(nick) in n_s:
                nick = f'Username{rnd.choice(["", ".", "_", "-"])}'
                nick += '{rnd.randint(1, 60000)}'

        nick2 = b(nick)
        client.send(nick2)

        nick2 = client.recv(BUF_S)

        n_s.add(nick2)
        c_s.add(client)

        print(f'Nickname of client <{client}> is',
              f'{nick}',
              end='\n\n')
        sleep(1)

        broadcast(c_s, b(f'User {nick} has connected.\n'))
        client.send(b('Connected to server.'))

        thd = thr.Thread(target=handle, args=(client, n_s, c_s))
        thd.start()


def main(port: int) -> int:
    """Función principal."""
    ret = 0

    try:
        srv = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        srv.bind((HOST, port))
        srv.listen()

        c_s, n_s = set(), set()

        sleep(2)
        print('Server running...')
        receive(srv, c_s, n_s)

    except KeyboardInterrupt:
        print('ABORTING...',
              end='\n\n',
              file=sys.stderr)
        srv.close()
        sleep(3)
        ret = -1

    except Exception:
        print('Something went wrong.',
              'ABORTING...',
              sep='\n',
              end='\n\n',
              file=sys.stderr)
        sleep(2)
        ret = 2

    # finally:
    #    srv.close()

    srv.close()
    sleep(2)
    return ret


if __name__ == '__main__':
    port_n = 0
    tries_n = 1

    while port_n <= 0:
        try:
            print('Select port:', end=' ')
            port_n = int(input().strip().lstrip('0'))

            if port_n <= 0:
                if tries_n >= MAX_TRIES:
                    print('You have exceeded the maximum amount of tries.',
                          'Aborting...',
                          sep='\n',
                          end='\n\n',
                          file=sys.stderr)
                    sleep(3)
                    sys.exit(2)
                else:
                    print(f'Invalid port \'{port_n}\'.',
                          'It cannot be less than 1!',
                          sep='\n',
                          file=sys.stderr)
                    sleep(2)
                    print(f'You have {MAX_TRIES - tries_n} tries left.',
                          end='\n\n',
                          file=sys.stderr)
                    sleep(2)
                    continue

        except KeyboardInterrupt:
            print('ABORTING...',
                  end='\n\n',
                  file=sys.stderr)
            sleep(3)
            sys.exit(-1)

        except Exception:
            if tries_n >= MAX_TRIES:
                print('You have exceeded the maximum amount of tries.',
                      'ABORTING...',
                      sep='\n',
                      end='\n\n',
                      file=sys.stderr)
                sleep(3)
                sys.exit(2)

            else:
                print('Something went wrong. Try again...',
                      file=sys.stderr)
                sleep(2)
                print(f'You have {MAX_TRIES - tries_n} tries left.',
                      end='\n\n',
                      file=sys.stderr)
                sleep(2)
                continue

        finally:
            tries_n += 1
            continue

    sys.exit(main(port_n))
