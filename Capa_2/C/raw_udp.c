#include <main.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	if (argc != 5) {
		printf("Missing arguments!\n");
		return 1;
	}

	char *buffer = (char*) malloc(sizeof(char) * PCKT_LEN);
	ip_head_t *ip = (ip_head_t *) buffer;
	udp_head_t *udp = (udp_head_t *) (buffer + sizeof(ip_head_t));
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

	// FALTA MUCHO...

	return 0;
}

static ush csum(const ush *buf, const ul nwords) {
	ul sum = 0;
	for (ul i = 0; i < nwords; i++)
		sum += *(buf + i);

	sum = (sum >> 16) + (sum &0xffff);
	sum += (sum >> 16);

	return (ush) (~sum);
}
