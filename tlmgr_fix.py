#!/usr/bin/python3
# Repeatedly attempt to compile the given .tex file,
# installing missing package as needed.
# usage:
#    tlmgr_fix filename.tex
import sys, re
import subprocess as s

def compile_while(filename):
    x = trycompile(filename)
    while x is not None:
        install(find(x))
        x = trycompile(filename)

def trycompile(filename):
    cmd = f'pdflatex -interaction nonstopmode {filename} | grep "LaTeX Error: File"'
    a = s.run([cmd], shell=True, stdout=s.PIPE, stderr=s.STDOUT)
    result = a.stdout.decode().split('\n')[0]
    if result == '':
        return None
    missing_pkg = re.findall("`(.*)'", result)[0]
    return missing_pkg

def find(pkg):
    cmd = f'tlmgr search --global --file "/{pkg}"'
    a = s.run([cmd], shell=True, stdout=s.PIPE, stderr=s.STDOUT)
    result = a.stdout.decode().split('\n')[-3][:-1]
    if len(result.split()) == 1:
        return result
    raise

def install(pkg):
    cmd = f'tlmgr install {pkg}'
    s.run([cmd], shell=True)

def update():
    s.run(['tlmgr update --self --all'], shell=True)
    s.run(['tlmgr path add'], shell=True)
    s.run(['fmtutil-sys --all'], shell=True)

def fix(pkg):
    install(find(pkg))
    update()

if __name__ == "__main__":
    compile_while(sys.argv[1])
    update()
