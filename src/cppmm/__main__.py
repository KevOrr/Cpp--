#!/usr/bin/env python3

from pathlib import Path

import click

import cppmm


@click.command(context_settings={'ignore_unknown_options': True})
@click.option('-o', 'outfile', metavar='OUTFILE', type=click.Path(), default=None,
              help='Output file (defaults to an appropriate filename based on INFILES)')
@click.option('--gcc-option', metavar='OPTION', multiple=True, type=str,
              help='Argument to be passed to g++. Can be used more than once')
@click.argument('infiles', nargs=-1, type=click.Path(exists=True, readable=True))
def main(infiles, outfile, gcc_option):
    if not infiles:
        return

    if not outfile:
        outfile = Path(infiles[0]).stem + '.c'

    cppmm.transpile(
        [Path(src) for src in infiles],
        Path(outfile),
        gcc_option
    )

if __name__ == '__main__':
    main()
