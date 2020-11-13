#!/usr/bin/env python3

import pytest

import subprocess
from pathlib import Path

TEST_DIR = Path(__file__).parent

def test_hello_world(tmp_path):
    subprocess.check_call(['cppmm', '-o', str(tmp_path/'main.c'), str(TEST_DIR/'hello_world/main.cpp')])
    subprocess.check_call(['gcc', '-o', str(tmp_path/'a.out'), str(tmp_path/'main.c'), '-lstdc++'])
    assert subprocess.check_output([str(tmp_path/'a.out')], text=True) \
        == 'Hello, world!\n'

def test_including(tmp_path):
    subprocess.check_call(['cppmm', '-o', str(tmp_path/'lib.c'), str(TEST_DIR/'including/lib.cpp')])
    subprocess.check_call(['cppmm', '-o', str(tmp_path/'main.c'), str(TEST_DIR/'including/main.cpp')])
    subprocess.check_call(['gcc', '-o', str(tmp_path/'a.out'),
                           str(tmp_path/'lib.c'), str(tmp_path/'main.c'),
                           '-lstdc++'])

    p = subprocess.Popen([str(tmp_path/'a.out')], text=True, stderr=subprocess.PIPE)
    stderr = p.stderr.read()
    ret = p.wait()
    assert stderr == 'Missing argument\n'
    assert ret == 1

    assert subprocess.check_output([str(tmp_path/'a.out'), 'asdfqwerghrut'], text=True) \
        == 'turhgrewqfdsa\n'
