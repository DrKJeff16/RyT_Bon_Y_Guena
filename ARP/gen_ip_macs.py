#!/usr/bin/env python
"""Generador de computadoras."""
import sys
import random as rnd


if __name__ == '__main__':
    n = 12
    ops = (n ** 3) + 1500
    all_ips_L = [f'192.168.{rnd.randint(0, 2)}.{rnd.randint(1, 48)}' for s in
                 range(ops)]
    all_ips = set(all_ips_L)
    all_hex = set()

    for s in range(ops):
        all_hex.add(':'.join(['%02x' % rnd.randint(0, 255) for _ in range(6)]))

    all_ips = list(set(rnd.sample(list(all_ips.copy()), n)))
    all_hex = list(set(rnd.sample(list(all_hex.copy()), n)))

    all_ips.sort(key=lambda x: int(x.split('.')[3]))
    all_ips.sort(key=lambda x: int(x.split('.')[2]))

    with open('./ip_macs.txt', 'w') as file:
        for ip, mac in zip(all_ips, all_hex):
            file.write(f'{ip},{mac}\n')

    sys.exit(0)
