#include "a.hpp"

#include <string>
#include <algorithm>

std::string reverse(std::string s) {
    std::string res = s;
    std::reverse(res.begin(), res.end());
    return res;
}
