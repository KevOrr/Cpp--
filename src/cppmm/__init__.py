from typing import List
from pathlib import Path
import subprocess
import sys
import os
import tempfile

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
    fd, tmpout = tempfile.mkstemp(suffix='.s')
    os.close(fd)

    cmd = ['g++', '-S', *gcc_options, '-o', tmpout, *map(str, sources)]
    subprocess.check_call(cmd)

    with open(tmpout, 'rb') as f:
        assembly: bytes = f.read()

    os.remove(tmpout)

    with open(dest, 'w') as f:
        f.write(f'__asm({cstr_literal(assembly)});\n')
