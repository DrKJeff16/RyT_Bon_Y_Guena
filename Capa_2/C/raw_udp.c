#include <main.h>
#include <stdlib.h>

const int ONE = 1;
const int *VAL = &ONE;
ush csum(const ush *buf, const ul nwords);

int main(int argc, char **argv) {
  if (argc != 5) {
    printf("Missing arguments!\n");
    return 1;
  }

  char *buffer = (char *)malloc(sizeof(char) * PCKT_LEN);
  ip_head_t *ip = (ip_head_t *)buffer;
  udp_head_t *udp = (udp_head_t *)(buffer + sizeof(ip_head_t));
  sockaddr_IN sin, din;
  memset(buffer, 0, PCKT_LEN);

  int sd = socket(PF_INET, SOCK_RAW, IPPROTO_UDP);

  if (sd < 0) {
    perror("socket() error.");
    return 1;
  }

  printf("socket() - Using SOCK_RAW socket. UDP protocol is OK.\n");
  sin.sin_family = AF_INET;
  din.sin_family = AF_INET;

  // Port numbers
  sin.sin_port = htons(atoi(argv[2]));
  din.sin_port = htons(atoi(argv[4]));

  // IP addresses
  sin.sin_addr.s_addr = inet_addr(argv[1]);
  din.sin_addr.s_addr = inet_addr(argv[3]);

<<<<<<< HEAD
  // Fabricate the IP header or we can use the
||||||| parent of 513c383 (Cosas nuevas.)
	// Fabricate the IP header or we can use the
=======
  // Fabricate the IP header or we can use the
  // standard header structures but assign our own values.
  ip->iph_ihl = 5;
  ip->iph_ver = 4;
  ip->iph_tos = 16; // Low delay
  ip->iph_len = sizeof(ip_head_t) + sizeof(udp_head_t);
  ip->iph_ident = htons(54321);
  ip->iph_ttl = 64;      // hops
  ip->iph_protocol = 17; // UDP
  // Source IP address, can use spoofed address here!!!
  ip->iph_sourceip = inet_addr(argv[1]);
  // The destination IP address
  ip->iph_destip = inet_addr(argv[3]);
>>>>>>> 513c383 (Cosas nuevas.)

<<<<<<< HEAD
  // standard header structures but assign our own values.
  ip->iph_ihl = 5;
  ip->iph_ver = 4;
  ip->iph_tos = 16; // Low delay
  ip->iph_len = sizeof(ip_head_t) + sizeof(udp_head_t);
  ip->iph_ident = htons(54321);
  ip->iph_ttl = 64;      // hops
  ip->iph_protocol = 17; // UDP
  // Source IP address, can use spoofed address here!!!
  ip->iph_sourceip = inet_addr(argv[1]);
  // The destination IP address
  ip->iph_destip = inet_addr(argv[3]);

  return 0;
||||||| parent of 513c383 (Cosas nuevas.)
// standard header structures but assign our own values.
ip->iph_ihl = 5;
ip->iph_ver = 4;
ip->iph_tos = 16; // Low delay
ip->iph_len = sizeof(ip_head_t) + sizeof(udp_head_t);
ip->iph_ident = htons(54321);
ip->iph_ttl = 64; // hops
ip->iph_protocol = 17; // UDP
// Source IP address, can use spoofed address here!!!
ip->iph_sourceip = inet_addr(argv[1]);
// The destination IP address
ip->iph_destip = inet_addr(argv[3]);

	return 0;
=======
  return 0;
>>>>>>> 513c383 (Cosas nuevas.)
}

<<<<<<< HEAD
ush csum(const ush *buf, const ul nwords) {
  ul sum = 0;
  for (ul i = 0; i < nwords; i++)
    sum += *(buf + i);
||||||| parent of 513c383 (Cosas nuevas.)
static ush csum(const ush *buf, const ul nwords) {
	ul sum = 0;
	for (ul i = 0; i < nwords; i++)
		sum += *(buf + i);
=======
static ush csum(const ush *buf, const ul nwords) {
  ul sum = 0;
  for (ul i = 0; i < nwords; i++)
    sum += *(buf + i);
>>>>>>> 513c383 (Cosas nuevas.)

  sum = (sum >> 16) + (sum & 0xffff);
  sum += (sum >> 16);

  return (ush)(~sum);
}
