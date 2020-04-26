#!/usr/bin/python3
import re
import subprocess as s
import sys

def compile_until_no_errors(filename):
    x = compile_once(filename)
    old_install = None
    while x is not None:
        new_install = find(x)
        if old_install == new_install:
            perr(f'{__file__.split("/")[-1]} got stuck in a loop, exiting')
            exit(1)
        old_install = new_install
        install(old_install)
        x = compile_once(filename)

def perr(*args):
    print(*args, file=sys.stderr)

def compile_once(filename):
    cmd = f'pdflatex -interaction nonstopmode {filename} | grep "LaTeX Error: File"'
    a = s.run([cmd], shell=True, encoding='utf-8', stdout=s.PIPE, stderr=s.STDOUT)
    result = a.stdout.split('\n')[0]
    if result == '':
        return None
    return re.findall("`(.*)'", result)[0]

def find(pkg) -> list:
    '''find dependencies for {pkg}'''
    cmd = f'tlmgr search --global --file "/{pkg}"'
    a = s.run([cmd], shell=True, encoding='utf-8', stdout=s.PIPE, stderr=s.PIPE)
    result = re.findall(r'^((?!tlmgr).*):', a.stdout, re.M)
    if len(result):
        return result
    perr(f'{__file__.split("/")[-1]} was unable to find {pkg}')
    perr(a.stderr)
    exit(1)

def install(pkgs:list):
    print(f'installing {" ".join(pkgs)}...')
    # s.run('tlmgr install'.split() + pkgs, stdout=s.PIPE, stderr=s.STDOUT)
    s.run(f'tlmgr install {" ".join(pkgs)} > /dev/null', shell=True)

def update():
    s.run('tlmgr update --self --all'.split())
    s.run('tlmgr path add'.split())
    s.run('fmtutil-sys --quiet --all > /dev/null', shell=True)

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

        HELPFUL TIP! If your version of texlive is older than some packages,
        you may experience checksum errors.
        Save time: upgrade texlive and carry on.

        This utility wraps tinytex, a minimal texlive distribution.
        See also: https://github.com/yihui/tinytex'''))
    p.add_argument('texfile', help='LaTeX document to compile')
    args = p.parse_args()
    compile_until_no_errors(args.texfile)
    update()
