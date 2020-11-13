#!/usr/bin/env python3

import pytest

import subprocess
from pathlib import Path

TEST_DIR = Path(__file__).parent

def test_hello_world(tmp_path):
    subprocess.check_call(['cppmm', TEST_DIR/'hello_world/main.cpp', '-o', tmp_path/'main.c'])
    subprocess.check_call(['g++', tmp_path/'main.c', '-o', tmp_path/'a.out'])
    assert subprocess.check_output([tmp_path/'a.out']) == b'Hello, world!\n'
