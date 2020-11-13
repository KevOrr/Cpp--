from typing import List
from pathlib import Path
import subprocess
import sys

def cstr_literal(s: bytes) -> str:
    '''
    Encode any `bytes` as a C string literal
    '''

    translate = {
        b'\a': r'\a',
        b'\b': r'\b',
        b'\t': r'\t',
        b'\n': r'\n',
        b'\v': r'\v',
        b'\f': r'\f',
        b'\r': r'\r',
        b'\"': r'\"',
        b'\\': r'\\',
        b'?':  r'\?', # Needed because of trigraphs
    }

    c_str = ''.join(
        translate.get(
            bytes([c]),
            chr(c) if c < 128 else rf'\x{c:02x}'
        )
        for c in s
    )

    return f'"{c_str}"'


def transpile(sources: List[Path], dest: Path, gcc_options: List[str]):
    cmd = ['g++', '-S', *gcc_options, '-o', '/dev/stdout', *map(str, sources)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    assembly: bytes = p.stdout.read()  # type: ignore  # dumb type error

    if p.wait() != 0:
        print('cppmm: error when running g++', file=sys.stderr)
        exit(1)

    with open(dest, 'w') as f:
        f.write(f'__asm({cstr_literal(assembly)});\n')
