#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ejercicio de emulación de ARP, para la clase de Redes y Telecomunicaciones.

* Autores: Michel Paola Osornio Torres, Guennadi Maximov Cortés
* Fecha de Creación: 12/10/2022
* Última Edición: 24/10/2022
"""
import sys
import random as rnd
from time import sleep
from collections import deque as dq


class Computadora:
    """Crea un objeto de tipo computadora."""

    def __init__(self, ip_addr: str, mac_addr: str, cid: int):
        """Método Constructor."""
        self.id = cid
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr

        self.pair = (self.id, self.ip_addr, self.mac_addr)
        self.conns = set()  # Con qué computadoras me he comunicado?
        self.conns.add(self.pair)

    def __eq__(self, other) -> bool:
        """Checa si pueden comunicarse dos computadoras."""
        return [int(val[0]) == int(val[1]) for k, val in
                enumerate(zip(list(self.ip_addr.split('.')),
                              list(other.ip_addr.split('.'))))
                ] in (list([True] * 4),
                      list([True] * 3) + [False])

    def __repr__(self) -> str:
        return f'"{self.pair[0]}": IP: {self.pair[1]}\tMAC: {self.pair[2]}\n'

    def __int__(self) -> int:
        return self.id

    def arp_table(self) -> None:
        """Imprime la tabla de ARP."""
        D = dq(self.conns)
        D.remove(self.pair)
        D.appendleft(self.pair)
        for name, ip, mac in D:
            print(f'{name}\t{ip}\t{mac}')

    def ping(self, other, count=None, bs=None) -> None:
        """Comunica con otra computadora.

        Si no hay una conexión entre estas dos computadoras, conectarlas
        insertando en sus conjuntos de conexiones respectivos.
        """
        if self != other:
            print(f'\'{int(self)}\' ({self.ip_addr})'
                  f'y \'{int(other)}\' ({other.ip_addr})',
                  'no pueden comunicarse!',
                  file=sys.stderr)
            return

        if other.pair not in self.conns or self.pair not in other.conns:
            self.conns.add(other.pair)
            other.conns.add(self.pair)

        if count is None:
            count = rnd.randint(5, 14)
        elif count <= 0:
            count = rnd.randint(5, 14)

        if bs is None:
            bs = rnd.choice([64, 32, 16, 8, 4, 2, 1, 128, 256, 512])
        elif bs <= 0:
            bs = rnd.choice([64, 32, 16, 8, 4, 2, 1, 128, 256, 512])

        for c in range(1, count + 1):
            t = float(rnd.randint(5, 10)) * (bs / (bs + 1)) / 11
            sleep(t)
            print(f'\tEnviado Paquete #{c}/{count} ({bs} bytes) de la',
                  f'dirección {self.ip_addr} a la dirección',
                  f'{other.ip_addr}, t={int(t*100)}ms')


def select_comp(comps: list, curr=None) -> int:
    """Selecciona una computadora."""
    if curr is not None and curr not in [int(c) - 1 for c in comps]:
        raise ValueError("")

    exc = curr

    while True:
        top = '|\tComputadora\t|\tIP\t|\tMAC\t|'
        print(top, '=' * len(top), sep='\n')

        for c in comps:
            print(f'|\t{int(c)}\t|\t{c.ip_addr}\t|\t{c.mac_addr}\t|')

        comp = input("Ingrese la ID de computadora que desee utilizar: ")
        comp = int(comp.strip().lstrip('0'))

        if exc is None:
            if comp in [int(c) for c in comps]:
                return int(comp) - 1
        elif exc is not None:
            if comp - 1 == exc:
                print(f'La computadora \'{comp}\' ya esta seleccionada.',
                      file=sys.stderr)
            elif comp in [int(c) for c in comps]:
                return int(comp) - 1
            else:
                print(f'La computadora \'{comp}\' no parece existir.',
                      file=sys.stderr)
        else:
            print(f'La computadora \'{comp}\' no parece existir.',
                  file=sys.stderr)


def select_op(curr: int, comps: list) -> bool:
    """Selecciona una operación."""
    while True:
        print('\nOperaciones Válidas:',
              '1) Comunicarse con otra máquina.',
              '2) Imprimir tabla ARP de máquina actual.',
              '\n\t0) Cambiar de máquina.',
              '-1) Salir del programa.',
              sep='\n\t',
              end='\n\n')
        op = int(input("Seleccione la operacion deseada: ").strip())

        if op == 0:
            # Indica que se quiere seleccionar otra máquina.
            return False

        if op == -1:
            # Indica que quiere salir del programa.
            return True

        if op == 1:
            # Elige un índice aleatorio `oth` de la lista de computadoras
            # En existencia `comps`
            oth = rnd.randrange(len(comps))

            # La computadora actual de índice `curr`
            # Invoca su método `ping()` con la otra
            # Computadora seleccionada de índice `oth`
            comps[curr].ping(comps[oth])

        elif op == 2:
            # Imprime la tabla ARP de la computadora seleccionada
            comps[curr].arp_table()


def main() -> int:
    """Función principal."""
    # Abrimos el archivo de las IPs y MACs
    with open('./ip_macs.txt', 'r') as file:
        ip_mac = [ln.strip().strip('\r').strip('\n').strip('\t').split(',')
                  for ln in file.readlines()]

    ip_L, mac_L = list(), list()

    for ip, mac in ip_mac:
        ip_L.append(ip)
        mac_L.append(mac)

    ip_L.sort(key=lambda x: int(x.split('.')[3]))
    ip_L.sort(key=lambda x: int(x.split('.')[2]))

    mac_L = rnd.sample(mac_L.copy(), len(mac_L))
    comp_act = None

    comps = [Computadora(ip, mac, id_c) for ip, mac, id_c in
             zip(ip_L, mac_L, list(range(1, len(ip_L) + 1)))]

    salir = False

    while not salir:
        comp_act = select_comp(comps, comp_act)
        salir = select_op(comp_act, comps)

    return 0


if __name__ == '__main__':
    sys.exit(main())
