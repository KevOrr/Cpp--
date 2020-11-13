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
