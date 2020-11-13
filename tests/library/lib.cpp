#include "lib.h"

#include <string.h>
#include <string>
#include <algorithm>

extern "C" char * reverse(const char *s) {
    std::string res = std::string(s);

    std::reverse(res.begin(), res.end());

    char *res_str = (char *) malloc(res.length() + 1);
    strncpy(res_str, res.c_str(), res.length() + 1);
    return res_str;
}
