/**
 * @file main.h
 * @author Guennadi Maximov (g.maxc.fox@protonmail.com)
 * @brief Archivo de Cabecera local.
 * @version 0.1
 * @date 2022-11-15
 *
 * @copyright Copyright (c) 2022
 *
 */

// Fuente: https://www.tenouk.com/Module43a.html
#ifndef MAIN_H
#define MAIN_H

#ifndef PCKT_LEN
#define PCKT_LEN 8192
#endif // PCKT_LEN

// TODO: Explicar Cada Inclusión de Header File (`*.h`)

// Librerías propias que acortan la talacha del `static typing` de C.
#include "ouraliases.h"

// Libs necesarias por defecto.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Libs de sockets y protocolos de comunicado.
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <sys/socket.h>

// TODO: Entender que es esto.
typedef struct IpHeader {
  uch iph_ihl : 5, iph_ver : 4;
  uch iph_tos;
  ush iph_len;
  ush iph_ident;
  uch iph_flag;
  ush iph_offset;
  uch iph_ttl;
  uch iph_protocol;
  ush iph_chksum;
  ui iph_sourceip;
  ui iph_destip;
} ip_head;

#endif // MAIN_H
