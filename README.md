![Tests](https://github.com/KevOrr/Cpp--/workflows/Tests/badge.svg)

# C++--

C++ to C transpiler

## Example

`main.cpp`:
```c++
#include <iostream>
int main() {
    std::cout << "Hello, world!" << std::endl;
}
```

```sh
$ poetry build
$ pip install dist/cppmm-0.1.0-py3-none-any.whl
$ c++-- main.cpp -o main.c
$ gcc main.c -o main -lstdc++
$ ./main
Hello, World!
```

## Proof of correctness

Let

- CPP ::= all valid C++ programs
- C ::= all valid C programs
- (p1 : CPP) ≅ (p2 : C) ::= `p1` and `p2` are semantically equivalent
- [[p : CPP]] : C ::= the interpretation of `p` under C++--

Then

| | Judgement | Evidence |
|-|-----------|----------|
|1| C++-- can't possibly work (i.e. ∀ (p : CPP), p ≇ [[p]])                | Assumption               |
|2| p1 ≇ [[p1]] → (p1 ≅ [[p1]] → ∀ (p : CPP), p ≅ [[p]])                 | by Principal of Explosion |
|3| p1 ≇ [[p1]]                                                            | by (1) and ∀-elim         |
|4| p1 ≅ [[p1]] → ∀ (p : CPP), p ≅ [[p]]                                 | by (2), (3), Modus Ponens |
|5| (∃ (p1 : CPP), p1 ≅ [[p1]]) → ∀ (p : CPP), p ≅ [[p]]                 | by (4) and ∃-elim         |
|6| (∃ (p : CPP), p ≅ [[p]]) → ∀ (p : CPP), p ≅ [[p]]                    | by (5) and ɑ-equiv        |
|7| C++-- works for `hello_world.cpp` above (i.e. ∃ (p : CPP), p ≅ [[p]]) | Inspection                |
|8| ∀ (p : CPP), p ≅ [[p]]                                                | by (6), (7), Modus Ponens |
