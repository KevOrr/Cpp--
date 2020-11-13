#include <iostream>

#include "lib.hpp"

int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cerr << "Missing argument" << std::endl;
        return 1;
    }

    std::cout << reverse(argv[1]) << std::endl;
}
