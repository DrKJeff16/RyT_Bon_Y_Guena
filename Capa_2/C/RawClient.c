#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <getopt.h>
#include <errno.h>
#include <sys/socket.h>
#include <net/ethernet.h>
#include <net/if_arp.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>
#include <linux/if.h>
#include <unistd.h>
#include <ctype.h>

#define ifaddr(x) (*(struct in_addr *) &x->ifr_addr.sa_data[sizeof sa.sin_port])
#define IFRSIZE ((int)(size * sizeof (struct ifreq)))

/* Carga Util */
typedef struct _inf {
	char carga[1024];
} info;

/*Limpia la variable  */
void LimpiaDatos(char *carga) {
	printf("\n");

	for (int i = 0; i < 1024; i++){
		carga[i] = '\0';
	}
}

/*Cambia la MAC de char a hexadecimal*/
void CharAHex(char *origen, char *destino) {
	int i = 0, j = 0, f = 1, hex;
	char a;

	while (i < 17) {
		a = origen[i];

		switch (a) {
			case 'A':
				f++;
				hex = 10;
				break;
			case 'B':
				f++;
				hex = 11;
				break;
			case 'C':
				f++;
				hex = 12;
				break;
			case 'D':
				f++;
				hex = 13;
				break;
			case 'E':
				f++;
				hex = 14;
				break;
			case 'F':
				f++;
				hex = 15;
				break;
			case ':':
				j++;
				hex = 0;
				break;
			default:
				f++;
				hex = atoi(&a);
				break;
		}

		if(!(f % 2)){
			destino[j] = hex * 16;
		} else {
			destino[j] += hex;
		}

		i++;
	}
}

/*Obtener MAC del host origen*/
unsigned char *localMAC(void) {
	unsigned char *u;
	int sockfd, size = 1;
	struct ifreq *ifr;
	struct ifconf ifc;
	// struct sockaddr_in sa;

	if (0 > (sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP))) {
		fprintf(stderr, "Cannot open socket.\n");
		exit(EXIT_FAILURE);
	}

	ifc.ifc_len = IFRSIZE;
	ifc.ifc_req = NULL;

	do {
		++size;

		if (NULL == (ifc.ifc_req = realloc(ifc.ifc_req, IFRSIZE))) {
			fprintf(stderr, "Out of memory.\n");
			exit(EXIT_FAILURE);
		}

		ifc.ifc_len = IFRSIZE;

		if (ioctl(sockfd, SIOCGIFCONF, &ifc)) {
			perror("ioctl SIOCFIFCONF");
			exit(EXIT_FAILURE);
		}

	} while (IFRSIZE <= ifc.ifc_len);

	ifr = ifc.ifc_req;

	for (;(char *) ifr < (char *) ifc.ifc_req + ifc.ifc_len; ++ifr) {
		if (ifr->ifr_addr.sa_data == (ifr+1)->ifr_addr.sa_data) {
			continue; /* duplicate, skip it */
		}

		if (ioctl(sockfd, SIOCGIFFLAGS, ifr)) {
			continue; /* failed to get flags, skip it */
		}

		if (0 == ioctl(sockfd, SIOCGIFHWADDR, ifr)) {
			switch (ifr->ifr_hwaddr.sa_family) {
				default:
					printf("\n");
					continue;

				case ARPHRD_NETROM:
				case ARPHRD_ETHER:
				case ARPHRD_PPP:
				case ARPHRD_EETHER:
				case ARPHRD_IEEE802:
				break;
			}

			u = (unsigned char *) &ifr->ifr_addr.sa_data;

			if (u[0] + u[1] + u[2] + u[3] + u[4] + u[5]) {
				printf("HW Address: %2.2x.%2.2x.%2.2x.%2.2x.%2.2x.%2.2x\n",
				u[0], u[1], u[2], u[3], u[4], u[5]);
			}
		}

		printf("\n");
	}

	close(sockfd);
	return u;
}

int main(void) {
	char MAC[17];
	char Datos[1024];

	LimpiaDatos(Datos);
	fflush(stdin);

	printf("******************BIENVENIDO AL EMISOR!!**************************\n");

	printf("Escriba la MAC destino (xx:xx:xx:xx:xx:xx): \n");
	gets(MAC);

	printf("Escriba el mensaje a enviar: ");
	gets(Datos);

	unsigned int i = 0;
	char a;

	while (i < 17) {
		a = toupper(MAC[i]);
		MAC[i] = a;
		i++;
	}
	/* socket */
	int sock_raw;

	/* Size of buffer */
	unsigned int buffer_size =
		// sizeof(struct info) + sizeof(struct ether_header);
		sizeof(info) + sizeof(struct ether_header);

	/* Buffer que contendra el paquete */
	unsigned char buffer[buffer_size];

	memset(buffer,0,buffer_size);

	/* Cabecera ethernet */
	struct ether_header *eth = (struct ether_header *) buffer;

	/* Datos */
	info *datos = (info *)(buffer + sizeof(struct ether_header));

	/* Direcciones MAC */
	// char *mac_orig = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06};
	char *mac_orig = (char *) localMAC();
	char mac_dest[6];
	CharAHex(MAC, mac_dest);

	/* Dispositivo/Interfaz  */
	char dev[5];
	strncpy(dev, "eth0", 5);

	/* Creacion del socket */
	if ((sock_raw = socket(AF_INET, SOCK_PACKET, ETH_P_ALL)) == -1) {
		perror("Error en socket()");
		exit(EXIT_FAILURE);
	}

	/* Rellena la cabecera ethernet */
	memcpy(eth->ether_dhost, mac_dest,ETHER_ADDR_LEN);
	memcpy(eth->ether_shost, mac_orig,ETHER_ADDR_LEN);
	eth->ether_type = 0x0004;

	/*Rellena la carga util*/
	strcpy(datos->carga,Datos);

	struct sockaddr addr;
	strncpy(addr.sa_data, dev, sizeof(addr.sa_data));

	/* Envio del paquete */
	if ((sendto(sock_raw, buffer, buffer_size, 0,
					&addr, sizeof(struct sockaddr)))==-1) {
		perror("Error en sendto()");
		exit(EXIT_FAILURE);
	}

	return 0;
}

