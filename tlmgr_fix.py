import subprocess as s

def find(pkg):
    cmd = f'tlmgr search --global --file "/{pkg}"'
    a = s.run([cmd], shell=True, stdout=s.PIPE, stderr=s.STDOUT)
    return a.stdout.decode().split('\n')[-3][:-1]

def install(pkg):
    cmd = f'tlmgr install {pkg}'
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
