#!/usr/bin/python3
import sys
import subprocess as s

def find(pkg):
    cmd = 'tlmgr search --global --file "/{}"'.format(pkg)
    a = s.run([cmd], shell=True, stdout=s.PIPE, stderr=s.STDOUT)
    result = a.stdout.decode().split('\n')[-3][:-1]
    if len(result.split()) != 1: raise
    return result

def install(pkg):
    cmd = 'tlmgr install {}'.format(pkg)
    s.run([cmd], shell=True)

def update():
    cmd0 = 'tlmgr update --self --all'
    cmd1 = 'tlmgr path add'
    cmd2 = 'fmtutil-sys --all'
    s.run([cmd0], shell=True)
    s.run([cmd1], shell=True)
    s.run([cmd2], shell=True)

def fix(pkg):
    install(find(pkg))
    update()

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        install(find(arg))
    update()
