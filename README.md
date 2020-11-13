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
$ cppmm main.cpp -o main.c
$ gcc main.c -o main -lstdc++
$ ./main
Hello, World!
```

## Proof of correctness

- DEFINITION CPP ::= all valid C++ programs
- DEFINITION C ::= all valid C programs
- DEFINITION sem_eq (p1 : CPP) (p2 : C) ::= if p1 and p2 are semantically equivalent then True else False
- DEFINITION $[[c]]$ means transforming the CPP program c using this script

- ASSUME This script can't possibly work (i.e. $\forall (p : \textrm{CPP}), \neg \textrm{sem_eq}~p~[[p]]$)
- ASSUME It works for the trivial input below (i.e. ∃ (p : CPP), sem_eq p [[p]])

| ¬sem_eq p1 [[p1]] -> (sem_eq p1 [[p1]] -> ∀ (p : CPP), sem_eq p [[p]]) | by Principal of Explosion          |
| ¬sem_eq p1 [[p1]]                                                      | by assumption 1 and ∀-elim         |
|  sem_eq p1 [[p1]] -> ∀ (p : CPP), sem_eq p [[p]]                       | by (1), (2), Modus Ponens          |
| (∃ (p1 : CPP), sem_eq p1 [[p1]]) -> ∀ (p : CPP), sem_eq p [[p]]        | by (3) and ∃-elim                  |
| (∃ (p : CPP), sem_eq p [[p]]) -> ∀ (p : CPP), sem_eq p [[p]]           | by (4) and ɑ-equiv                 |
| ∀ (p : CPP), sem_eq p [[p]]                                            | by (5), assumption 2, Modus Ponens |
