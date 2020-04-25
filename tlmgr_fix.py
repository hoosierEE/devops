#!/usr/bin/python3
import re
import subprocess as s
import sys

def compile_until_no_errors(filename):
    x = compile_once(filename)
    while x is not None:
        install(find(x))
        x = compile_once(filename)

def compile_once(filename):
    cmd = f'pdflatex -interaction nonstopmode {filename} | grep "LaTeX Error: File"'
    a = s.run([cmd], shell=True, stdout=s.PIPE, stderr=s.STDOUT)
    result = a.stdout.decode().split('\n')[0]
    if result == '':
        return None
    return re.findall("`(.*)'", result)[0]

def find(pkg):
    cmd = f'tlmgr search --global --file "/{pkg}"'.split()
    a = s.run(cmd, stdout=s.PIPE, stderr=s.STDOUT)
    result = a.stdout.decode().split('\n')[-3][:-1]
    if len(result.split()) == 1:
        return result
    print(f'Unable to find {pkg}')
    print(a.stdout, file=sys.stderr)
    exit(1)

def install(pkg):
    s.run(f'tlmgr install {pkg}'.split())

def update():
    s.run('tlmgr update --self --all'.split())
    s.run('tlmgr path add'.split())
    s.run('fmtutil-sys --all'.split())

if __name__ == "__main__":
    import argparse as a
    import textwrap
    p = a.ArgumentParser(
        prog='auto_tinytex',
        formatter_class=a.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Installs missing packages until your LaTeX document compiles.
        This allows for installing only what the document requires,
        and saves space compared to installing texlive-full/extra etc.

        This utility wraps tinytex, a minimal texlive distribution.
        See also: https://github.com/yihui/tinytex'''))
    p.add_argument('texfile', help='LaTeX document to compile')
    args = p.parse_args()
    compile_until_no_errors(args.texfile)
    update()
