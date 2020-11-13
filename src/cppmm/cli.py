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
                     ('.cc', '.cp', '.cxx', '.cpp', '.c++', '.c', '.i', '.ii', '.s', '.o')):
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

        else:
            gcc_args.append(opt1)

    subprocess.check_call(['gcc', *gcc_args, '-lstdc++'])


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
