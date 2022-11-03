#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor de Chat."""
import socket as sock
import string as s
import sys
import threading as thr
from time import sleep
from typing import AnyStr, List, NoReturn, Optional, Tuple, Union

HOST = '127.0.0.1'
ENC = 'utf-8'
MAX_TRIES = 5


def validate_nick(n_s: str) -> Tuple[bool, Optional[str]]:
    """Validate a nickname."""
    u = ''.join(sorted([c for c in s.punctuation if c not in '_.-']))
    u += '\n'
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

    return True, ''


def broadcast(c_l: List[sock.socket], msg: bytes):
    """Broadcast a Message"""
    for c_h in c_l:
        c_h.send(msg)


def recieve(srv: sock.socket,
            c_l: List[sock.socket],
            n_l: List[bytes]) -> Tuple:
    """Recieve a Message"""
    while True:
        nick = ''
        invalid_nick = True
        tries = 0
        client, addr = srv.accept()
        print(f'Connection established with \'{str(addr)}\'')

        while invalid_nick and tries < MAX_TRIES:
            try:
                nick = input('Insert your Nickname').strip()
                validated, reason = validate_nick(nick)

                if not validated:
                    tries += 1

                    if tries == MAX_TRIES:
                        print('You have exceeded the amount of tries.',
                              'Aborting...',
                              sep='\n',
                              file=sys.stderr)

                        srv.close()
                        sleep(3)
                        sys.exit(2)

                    else:
                        print(f'Invalid nickname!\n\tReason: "{reason}"',
                              f'You have {MAX_TRIES - tries} tries left',
                              sep='\n',
                              file=sys.stderr)
                        sleep(3)
                        print('Try again...',
                              end='\n\n',
                              file=sys.stderr)
                        sleep(1)
                        continue

            except KeyboardInterrupt:
                print('ABORTING...',
                      file=sys.stderr)

                srv.close()
                sleep(3)
                sys.exit(-1)

            except Exception:
                print('SOMETHING WENT WRONG',
                      'ABORTING...',
                      sep='\n',
                      file=sys.stderr)

                srv.close()
                sleep(3)
                sys.exit(1)

        nick2 = bytes(nick, encoding=ENC)

        client.send(nick2)

        nick2 = client.recv(1024)
        n_l.append(nick2)
        c_l.append(client)


def main(port: int) -> int:
    """Función principal."""
    ret = 0

    srv = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    try:
        srv.bind((HOST, port))
        srv.listen()

    except KeyboardInterrupt:
        print('ABORTING...',
              end='\n\n',
              file=sys.stderr)
        srv.close()
        sleep(3)
        ret = -1

    except Exception:
        print('Something went wrong!',
              'ABORTING...',
              sep='\n',
              end='\n\n',
              file=sys.stderr)
        sleep(2)
        ret = 1

    finally:
        srv.close()

    return ret


if __name__ == '__main__':
    port_n = 0
    tries_n = 1

    while port_n <= 0 and tries_n < MAX_TRIES:
        try:
            port_n = int(input("Select port_n: ").strip().lstrip('0'))

            if port_n <= 0:
                if tries_n >= MAX_TRIES:
                    print('You have exceeded the maximum amount of tries_n.',
                          'Aborting...',
                          sep='\n',
                          end='\n\n',
                          file=sys.stderr)
                    sleep(3)
                    sys.exit(2)
                else:
                    print(f'Invalid Port_N "{port_n}". It cannot be less than 1!',
                          end='\n\n',
                          file=sys.stderr)
                    sleep(1)
                    print(f'You have {MAX_TRIES - tries_n} left...',
                          file=sys.stderr)
                    sleep(2)
                    continue

        except KeyboardInterrupt:
            print('ABORTING...',
                  sep='\n\n',
                  file=sys.stderr)
            sleep(3)
            sys.exit(-1)

        except Exception:
            if tries_n >= MAX_TRIES:
                print('You have exceeded the maximum amount of tries_n.',
                      'Aborting...',
                      sep='\n',
                      end='\n\n',
                      file=sys.stderr)
                sleep(3)
                sys.exit(2)

            else:
                print('Something went wrong. Try again...',
                      file=sys.stderr)
                sleep(1)
                print(f'You have {MAX_TRIES - tries_n} left...',
                      file=sys.stderr)
                sleep(3)
                continue

        finally:
            tries_n += 1
            continue

    sys.exit(main(port_n))
