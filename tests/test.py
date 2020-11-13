#!/usr/bin/env python3

import subprocess
import sys

import pytest

def test_hello_world(tmp_path):
    subprocess.check_call([sys.executable, './cppmm.py', 'hello_world/main.cpp', '-o', tmp_path/'main.c'])
    subprocess.check_call(['g++', tmp_path/'main.c', tmp_path/'a.out'])
    assert subprocess.check_output([tmp_path/'a.out']) == 'Hello, world!\n'
