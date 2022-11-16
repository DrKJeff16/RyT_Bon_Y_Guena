/**
 * @file main.h
 * @author Guennadi Maximov (g.maxc.fox@protonmail.com)
 * @brief Archivo de Cabecera local.
 * @version 0.1
 * @date 2022-11-16
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
	uch iph_ihl:5, iph_ver:4;
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
} ip_head_t;

// TODO: Entender que es esto.
typedef struct UdpHeader {
	ush udph_srcport;
	ush udph_destport;
	ush udph_len;
	ush udph_chksum;
} udp_head_t;

// TODO: Entender que es esto.
typedef struct TcpHeader {
	ush tcph_srcport;
	ush tcph_destport;
	ui tcph_seqnum;
	ui tcph_acknum;
	uch tcph_reserved:4, tcph_offset:4;
	// uch tcph_flags;

	ui tcp_res1:4,      /*little-endian*/
		tcph_hlen:4,     /*length of tcp header in 32-bit words*/
		tcph_fin:1,      /*Finish flag "fin"*/
		tcph_syn:1,       /*Synchronize sequence numbers to start a connection*/
		tcph_rst:1,      /*Reset flag */
		tcph_psh:1,      /*Push, sends data to the application*/
		tcph_ack:1,      /*acknowledge*/
		tcph_urg:1,      /*urgent pointer*/
		tcph_res2:2;

	ush tcph_win;
	ush tcph_chksum;
	ush tcph_urgptr;
} tcp_head_t;

typedef struct sockaddr_in sa_in;

static int ONE = 1;
static const int *VAL = &ONE;

ush csum(ush *buf, int nwords);

#endif // MAIN_H
