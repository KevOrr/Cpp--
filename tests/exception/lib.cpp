#include "lib.h"

#include <string.h>
#include <string>
#include <algorithm>
#include <iostream>

extern "C" char * reverse(const char *s, int exception_unhandled) {
    std::string res = std::string(s);

    if (exception_unhandled) {
        throw 15;
    } else {
        try {
            throw 15;
        } catch (int& e) {
            std::cout << e << std::endl;
        }
    }

    std::reverse(res.begin(), res.end());

    char *res_str = (char *) malloc(res.length() + 1);
    strncpy(res_str, res.c_str(), res.length() + 1);
    return res_str;
}
