#include <errno.h>
#include <features.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <net/if.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <net/if_arp.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#define ifaddr(x) (*(struct in_addr *)&x->ifr_addr.sa_data[sizeof sa.sin_port])
#define IFRSIZE ((int)(size * sizeof(struct ifreq)))

unsigned char *u2;

unsigned char *localMAC (void) {
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

  for (; (char *)ifr < (char *)ifc.ifc_req + ifc.ifc_len; ++ifr) {
    if (ifr->ifr_addr.sa_data == (ifr + 1)->ifr_addr.sa_data) {
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

      u = (unsigned char *)&ifr->ifr_addr.sa_data;

      if (u[0] + u[1] + u[2] + u[3] + u[4] + u[5]) {
        printf("Su HW Address es: %2.2x.%2.2x.%2.2x.%2.2x.%2.2x.%2.2x\n", u[0],
               u[1], u[2], u[3], u[4], u[5]);
      }
    }

    printf("\n");
  }

  close(sockfd);
  return u;
}

int CreateRawSocket(int protocol_to_sniff) {
  int rawsock;

  if ((rawsock = socket(PF_PACKET, SOCK_RAW, htons(protocol_to_sniff))) == -1) {
    perror("Error creating raw socket: ");
    exit(-1);
  }

  return rawsock;
}

int BindRawSocketToInterface(char *device, int rawsock, int protocol) {
  struct sockaddr_ll sll;
  struct ifreq ifr;

  bzero(&sll, sizeof(sll));
  bzero(&ifr, sizeof(ifr));

  /* First Get the Interface Index  */
  strncpy((char *)ifr.ifr_name, device, IFNAMSIZ);

  if ((ioctl(rawsock, SIOCGIFINDEX, &ifr)) == -1) {
    printf("Error getting Interface index !\n");
    exit(-1);
  }

  /* Bind our raw socket to this interface */
  sll.sll_family = AF_PACKET;
  sll.sll_ifindex = ifr.ifr_ifindex;
  sll.sll_protocol = htons(protocol);

  if ((bind(rawsock, (struct sockaddr *)&sll, sizeof(sll))) == -1) {
    perror("Error binding raw socket to interface\n");
    exit(-1);
  }

  return 1;
}

void PrintPacketInHex(unsigned char *packet, int len) {

  /*struct ethhdr *ethernet_header;
  if (len > (int) sizeof(struct ethhdr)) {
    ethernet_header = (struct ethhdr *) packet;*/

  if (packet[0] == u2[0] && packet[1] == u2[1] && packet[2] == u2[2] &&
      packet[3] == u2[3] && packet[4] == u2[4] && packet[5] == u2[5]) {

    unsigned char *p = packet;
    printf("\n\n--------Inicio----\n\n");

    // while (len--) {
    while (len-- && *p != '\0') {
      printf("%c ", *p);
      p++;
    }

    printf("\n\n--------Fin-----\n\n");
  }
  /*} else {
    printf("Packet size too small!\n");
  }*/
}

void PrintInHex(char *mesg, unsigned char *p, int len) {
  printf("%s", mesg);

  while (len--) {
    printf("%.2x ", *p);
    p++;
  }
}

void ParseEthernetHeader(unsigned char *packet, int len) {
  struct ethhdr *ethernet_header;
  if (len > (int)sizeof(struct ethhdr)) {
    if (packet[0] == u2[0] && packet[1] == u2[1] && packet[2] == u2[2] &&
        packet[3] == u2[3] && packet[4] == u2[4] && packet[5] == u2[5]) {

      ethernet_header = (struct ethhdr *)packet;

      /* First set of 6 bytes are Destination MAC */
      PrintInHex("Destination MAC: ", ethernet_header->h_dest, 6);
      printf("\n");

      /* Second set of 6 bytes are Source MAC */
      PrintInHex("Source MAC: ", ethernet_header->h_source, 6);
      printf("\n");

      /* Last 2 bytes in the Ethernet header are the protocol it carries */
      PrintInHex("Protocol: ", (void *) &ethernet_header->h_proto, 2);
      printf("\n");
    }

  } else {
    printf("Packet size too small !\n");
  }
}

int main(int argc, char **argv) {
  argc--;

  if (argc < 2) {
    fprintf(stderr, "Not enough arguments given: %d\n", argc);
    return 1;
  }

  if (argc > 2) {
    fprintf(stderr, "Too many arguments given: %d\n", argc);
    return 1;
  }

  int raw = SOCK_RAW;
  unsigned char packet_buffer[2048];
  int len;
  int packets_to_sniff;
  struct sockaddr_ll packet_info;
  unsigned int packet_info_size = sizeof(packet_info);

  u2 = localMAC();

  /* create the raw socket */
  raw = CreateRawSocket(ETH_P_IP);

  /* Bind socket to interface */
  BindRawSocketToInterface(argv[1], raw, ETH_P_ALL);

  /* Get number of packets to sniff from user */
  packets_to_sniff = atoi(argv[2]);

  /* Start Sniffing and print Hex of every packet */
  // while (1)
  while (packets_to_sniff--) {
    if ((len = recvfrom(raw, packet_buffer, 2048, 0,
                        (struct sockaddr *)&packet_info, &packet_info_size)) ==
        -1) {
      perror("Recv from returned -1: ");
      exit(-1);
    } else {
      /* Packet has been received successfully !! */
      PrintPacketInHex(packet_buffer, len);

      /* Parse Ethernet Header */
      ParseEthernetHeader(packet_buffer, len);
    }
  }

  return 0;
}
