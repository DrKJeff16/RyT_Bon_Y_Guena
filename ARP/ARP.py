"""
Ejercicio de simulación de tablas ARP.

Para la clase de Redes y Telecomunicaciones.

* Autores: Michel Paola Osornio Torres, Guennadi Maximov Cortés
* Fecha de Creación: 12/10/2022
* Última Edición: 11/11/2022
"""
import sys
import random as rnd
from time import sleep
from collections import deque as dq
from typing import List, Set, Tuple


class Computadora:
    """Objeto de tipo computadora."""

    # IGNORAR: Utilizado para tener autocompletado y diagnósticos
    #          en el editor.
    cid: int
    ip_addr: str
    mac_addr: str
    table_set: Set[Tuple[int, str, str]]

    def __init__(self, ip_addr, mac_addr, cid):
        """Método constructor de un objeto de tipo computadora.

        Invocado al crear una nueva instancia:
        `comp_1 = Computadora('192.168.0.1', '....', 3)`
        """
        # ID de la instancia, usado también como índice,
        # Pero entonces su uso es `indice = computadora_n.cid - 1`.
        self.cid = cid

        # Direcciones IP y MAC de la instancia, ambas almacenadas en
        # Forma de cadena.
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr

        # Conjunto que almacena las computadoras con las que la instancia
        # Se ha comunicado exitosamente, i.e. la tabla ARP.
        self.table_set = set()

        # Agrega a esta instancia por defecto.
        self.table_set.add(self.pair())

    def pair(self) -> Tuple[int, str, str]:
        """Retorna la tupla `(cid, ip_addr, mac_addr)` de la instancia."""
        return self.cid, self.ip_addr, self.mac_addr

    def __eq__(self, other) -> bool:
        """Compara a dos objetos de la clase Computadora a nuestro gusto.

        Es decir, manipulamos el operador de igualdad `==`,
        el cual compara de la forma dada por esta función
        especial `__eq__`.
        """
        # Primero almacenamos las direcciones IP, en forma de lista
        # Separando por cada `.`.
        ip_1 = self.ip_addr.split('.')
        ip_2 = other.ip_addr.split('.')

        # Crearemos una lista en la que se almacenarán las comparaciones
        # Ordenadas, de izquierda a derecha, de ambas direcciones IP.
        lista_bools = list()

        # Iteramos utilizando las funciones
        # `enumerate()` y `zip()` para que nos dé, por cada iteración,
        # La tupla `(ind, par)`, donde `ind` es el índice, y
        # `par` es una tupla que contiene los `ind`-ésimos elementos
        # De ambas listas `ip_1` e `ip_2`:
        # `[(ip_1[0], ip_2[0]), (ip_1[1], ip_2[1]), ...]`.
        for num1, num2 in zip(ip_1, ip_2):
            # Agrega al final de `lista_bools` `True` o `False`
            # Si coinciden o no, respectivamente.
            lista_bools.append(int(num1) == int(num2))

        # Convierte `lista_bools` a una tupla.
        lista_bools = tuple(lista_bools.copy())

        # Dos posibilidades para que se puedan comunicar
        # Dos computadoras, en orden:
        #     1) La IP es exactamente la misma.
        #     2) La IP es distinta en el último valor, pero
        #        se encuentra en la misma red.
        valores_true = ((True, True, True, True), (True, True, True, False))

        # Retorna si `lista_bools` es alguna de las dos tuplas anteriores o no.
        return lista_bools in valores_true

    def __repr__(self) -> str:
        """Indica cómo se presenta el objeto al ser imprimido.

        e.g. `print(comp_n)`.
        """
        # Retorna una cadena formateada al invocar `print()`.
        return f'{self.pair()[0]}: IP:{self.pair()[1]}\tMAC:{self.pair()[2]}\n'

    def __int__(self) -> int:
        """Simplemente retorna `self.cid` al convertir en `int` la instancia.

        e.g. `indice = int(comp_n) - 1`.
        """
        return self.cid

    def arp_table(self) -> None:
        """Imprime la tabla de ARP de la instancia."""
        # Creamos una cola doble, importada como la clase `dq`.
        # A este objeto `D` se le asigna la cola doble construida
        # A partir de la tabla ARP `self.table_set`.
        D = dq(self.table_set)

        # Quitamos la computadora de `D`, para ponerla al principio
        # (`D.appendleft()`) de la cola.
        D.remove(self.pair)
        D.appendleft(self.pair)

        # Imprimimos cada tupla formateada de cada computadora
        # En la tabla ARP.
        for name, ip, mac in D:
            print(f'| {name} | {ip} | {mac} |')

    def ping(self, other) -> None:
        """Comunica la computadora actual con otra y actualizar ARP.

        Si las computadoras no pertenecen a la misma red, i.e.
        `comp_x != comp_y`, esto quiere decir que no se pueden comunicar
        entre ellas, dado el método `__eq__`.
        """
        # Ver si la instancia actual `self` puede comunicarse con
        # La otra `other`
        if self != other:
            print(f'{int(self)} ({self.ip_addr})'
                  f'y {int(other)} ({other.ip_addr})',
                  'no pueden comunicarse!')

            # Retornar vacío
            return

        # Si alguna computadora no se encuentra en la tabla ARP de la otra,
        # Agregar una a la tabla de la otra.
        if any([other.pair not in self.table_set,
                self.pair not in other.table_set]):
            self.table_set.add(other.pair)
            other.table_set.add(self.pair)

        # Emular el comando de terminal `ping`, enviando 10 mensajes cada medio
        # Segundo
        n_bytes = 64
        count = 10
        t = .5

        for c in range(count):
            sleep(t)
            print(f'\tEnviado Paquete #{c} de {count + 1} ({n_bytes} bytes):',
                  f'{self.ip_addr} ===> {other.ip_addr}.',
                  f't={int(t * 100)}ms')


def select_comp(l_comps: List[Computadora], curr=-1) -> int:
    """Menú de selección de computadoras.

    El parámetro `curr` consiste en indicar el índice ó `cid` de la
    computadora, pero empezando en 0 en lugar de 1.
    Cuando no hay computadora seleccionada, `curr` es -1 por defecto.
    """
    delay = 0.2

    # Crear un bucle sin terminar que, por cada iteración, se vuelva a
    # Pedir entrada de usuario hasta que sea válida.
    while True:
        sleep(delay)
        top = '\n|\tComputadora\t|\tIP\t|\tMAC\t|'

        # Imprime el tope de la tabla.
        print(top)

        for c in l_comps:
            # Por cada computadora en la lista de todas las computadoras
            # (`l_comps`), imprime una fila de la tabla.
            sleep(delay)
            print(f'|\t#{int(c)}\t|\t{c.ip_addr}\t|\t{c.mac_addr}\t|')

        print('\n\nIngrese la ID de la computadora que desee utilizar:',
              end=' ')
        comp = input().strip()
        comp = int(comp)

        if comp in [int(c) for c in l_comps]:
            return int(comp) - 1

        if comp - 1 == curr:
            print(f'La computadora #{comp} ya esta seleccionada.')
        else:
            print(f'La computadora #{comp} no parece existir.')


def select_op(curr: int, comps: List[Computadora]) -> bool:
    """Selecciona una operación."""
    # TODO: Explicar.
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
    # TODO: Explicar.
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
