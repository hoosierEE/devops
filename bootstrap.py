# $ python3 devops.py
from platform import machine as mach
import subprocess as s
import sys
cmds = {
    update: 'sudo apt-get update',
    apt: 'sudo apt-get install -y',
    git: 'git clone',
    gitrec: 'git clone --recursive',
    curl: 'curl -O',
    jver: 'j807_{}.deb'.format(['amd','arm'][mach()=='aarch64']),
    dpkg: 'sudo dpkg -i',
}

targets = {
    'emacs': [
        (cmds.apt, 'emacs25-nox unifont'),
    ],
    'xinu': [
        (cmds.apt, 'qemu gawk bison flex libz-dev gcc-arm-none-eabi make'),
        (cmds.gitrec, 'git@github.iu.edu:ashroyer/xinu-s19.git'),
    ],
    'k': [
        (cmds.git, 'git@github.com:kevinlawler/kona.git'),
    ],
    'j': [
        (cmds.curl, 'http://www.jsoftware.com/download/j807/install/'+jver),
        (cmds.dpkg, jver),
    ],
    'e110': [
        (cmds.apt, 'python3-pip'),
        (cmds.pip3, 'myhdl'),
    ],
}
longest = max(map(len, targets))

args = sys.argv[1:]
usage = '''
usage: python3 {} <options>

options:
{}'''.format(sys.argv[0], ''.join([
    ' {}:{} apt-get install {}\n'
    .format(k, ' '*(longest-len(k)), all_dicts[k]) for k in apt_pkgs]))

def update(): shell('sudo apt-get update')
def shell(cmd): s.run([cmd], shell=True)
def run(target):
    for cmd in target:
        shell(' '.join(cmd))

if __name__ == "__main__":
    if sum([int(a in args) for a in set(apt_pkgs)]):
        update()
        for a in args:
            apt(apt_pkgs[a])
    else:
        print(usage)
