import subprocess as s

def find(pkg):
    cmd = f'tlmgr search --global --file "/{pkg}"'
    a = s.run([cmd], shell=True, stdout=s.PIPE, stderr=s.STDOUT)
    return a.stdout.decode().split('\n')[-3][:-1]

def install(pkg):
    cmd = f'tlmgr install {pkg}'
    s.run([cmd], shell=True)
