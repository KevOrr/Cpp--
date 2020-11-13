#!/usr/bin/env python3

import pytest

import subprocess
from pathlib import Path

TEST_DIR = Path(__file__).parent

def test_hello_world(tmp_path):
    subprocess.check_call(['cppmm', str(TEST_DIR/'hello_world/main.cpp'), '-o', str(tmp_path/'main.c')])
    subprocess.check_call(['g++', str(tmp_path/'main.c'), '-o', str(tmp_path/'a.out')])
    assert subprocess.check_output(tmp_path/'a.out', text=True) \
        == 'Hello, world!\n'
