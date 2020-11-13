#!/usr/bin/env python3

from pathlib import Path
import subprocess
from typing import List

import click

import cppmm


@click.command(context_settings={'ignore_unknown_options': True},
               help='C++ compiler that uses C++-- as a frontened, and GCC as a backend')
@click.argument('arguments', nargs=-1)
def compile(arguments):
    cppmm_options: List[str] = []
    skip = 0
    for opt in arguments:
        if skip > 0:
            skip -= 1
            continue

        if opt == '-o':
            skip = 1
            continue

        elif opt.startswith('-'):
            cppmm_options.append(opt)

        # Absolutely inelegant hack, because I don't feel like learning and
        # specifying ALL of gcc's options
        elif not any(opt.lower().endswith(suffix) for suffix in
                     ('.cc', '.cp', '.cxx', '.cpp', '.c++', '.c', '.i', '.ii', '.s')):
            cppmm_options.append(opt)


    gcc_args: List[str] = []
    skip = 0
    for opt1, opt2 in zip(arguments, arguments[1:] + (None,)):
        if skip > 0:
            skip -= 1
            continue

        if opt1 == '-o':
            gcc_args += [opt1, opt2]
            skip = 1
            continue

        elif any(opt1.lower().endswith(suffix) for suffix in ('.cc', '.cp', '.cxx', '.cpp', '.c++', '.ii')):
            cfile = Path(opt1).stem + '.c'
            cppmm.transpile(
                [Path(opt1)],
                Path(cfile),
                cppmm_options
            )
            gcc_args.append(cfile)

        elif opt1.startswith('-std'):
            if opt1 == '-std':
                std = opt2
                skip = 1
            else:
                std = opt1.partition('=')[2]

            translation = {
                'c++98': 'c11',
                'c++03': 'c11',
                'gnu++98': 'gnu11',
                'gnu++03': 'gnu11',
                'c++11': 'c11',
                'c++0x': 'c11',
                'gnu++11': 'gnu11',
                'gnu++0x': 'gnu11',
                'c++14': 'c11',
                'c++1y': 'c11',
                'gnu++14': 'gnu11',
                'gnu++1y': 'gnu11',
                'c++17': 'c17',
                'c++1z': 'c17',
                'gnu++17': 'gnu17',
                'gnu++1z': 'gnu17',
                'c++20': 'gnu2x',
                'c++2a': 'gnu2x',
                'gnu++20': 'gnu2x',
                'gnu++2a': 'gnu2x',
            }
            gcc_args.append('-std=' + translation.get(std, 'gnu17'))

        else:
            gcc_args.append(opt1)

    subprocess.check_call(['gcc', *gcc_args, '-lstdc++', '-lm'])


@click.command(context_settings={'ignore_unknown_options': True},
               help='C++ to C transpiler')
@click.option('-o', 'outfile', metavar='OUTFILE', type=click.Path(), default=None,
              help='Output file (defaults to an appropriate filename based on INFILES)')
@click.option('--g++-option', 'gpp_option', metavar='OPTION', multiple=True, type=str,
              help='Argument to be passed to g++. Can be used more than once')
@click.argument('infiles', nargs=-1, type=click.Path(exists=True, readable=True))
def transpile(infiles: List[Path], outfile: Path, gpp_option: List[str]):
    if not infiles:
        return

    if not outfile:
        outfile = Path(infiles[0]).stem + '.c'

    cppmm.transpile(
        [Path(src) for src in infiles],
        Path(outfile),
        gpp_option
    )
