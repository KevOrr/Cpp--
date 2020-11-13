#include <stdlib.h>
#include <stdio.h>

#include "lib.h"

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fputs("Missing argument\n", stderr);
        return 1;
    }

    char *rev = reverse(argv[1], atoi(argv[2]));
    puts(rev);
    free(rev);
}
