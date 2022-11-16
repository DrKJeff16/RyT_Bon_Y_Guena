#include <main.h>

int main(int argc, char **argv) {
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
