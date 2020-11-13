#!/usr/bin/env python3

from pathlib import Path
import subprocess
from typing import List

import click

import cppmm


@click.command(context_settings={'ignore_unknown_options': True},
               help='C++ compiler that uses C++-- as a frontened, and GCC as a backend')
@click.option('-o', 'outfile', metavar='OUTFILE', type=click.Path(), default='a.out',
              help='Output file')
@click.option('--c++---option', 'cppmm_option', metavar='OPTION', multiple=True, type=str,
              help='Argument to be passed to c++--. Can be used more than once')
@click.option('--gcc-option', 'gcc_option', metavar='OPTION', multiple=True, type=str,
              help='Argument to be passed to gcc. Can be used more than once')
@click.argument('infiles', nargs=-1, type=click.Path(exists=True, readable=True))
def compile(infiles: List[Path], outfile: Path, cppmm_option: List[str], gcc_option: List[str]):
    if not infiles:
        return

    objects = []

    for infile in infiles:
        if not any(infile.lower().endswith(suffix) for suffix in ('.cc', '.cp', '.cxx', '.cpp', '.c++')):
            objects.append(infile)
        else:
            cfile = Path(infile).stem + '.c'
            cppmm.transpile(
                [Path(infile)],
                Path(cfile),
                cppmm_option
            )
            objects.append(cfile)

    subprocess.check_call(['gcc', *gcc_option, '-o', str(outfile), *map(str, objects), '-lstdc++'])


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
