# $ python3 devops.py
from platform import machine as mach
import subprocess as s
import sys
apt = 'sudo apt-get install -y'
git = 'git clone'
gitrec = 'git clone --recursive'
curl = 'curl -O'
jver = 'j807_{}.deb'.format(['amd','arm'][mach()=='aarch64'])
dpkg = 'sudo dpkg -i'

targets = {
    'emacs': [
        apt, 'emacs25-nox unifont',
    ],
    'xinu': [
        apt, 'qemu gawk bison flex libz-dev gcc-arm-none-eabi make',
        gitrec, 'git@github.iu.edu:ashroyer/xinu-s19.git',
    ],
    'k': [
        git, 'git@github.com:kevinlawler/kona.git',
    ],
    'j': [
        curl, 'http://www.jsoftware.com/download/j807/install/'+jver,
        dpkg, jver,
    ],
    'e110': [
        apt, 'python3-pip',
        pip3, 'myhdl',
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
def apt(cmd): shell('sudo apt-get install -y '+cmd)
def git(repo, newname = ''): shell('git clone '+repo+' '+newname)

if __name__ == "__main__":
    if sum([int(a in args) for a in set(apt_pkgs)]):
        update()
        for a in args:
            apt(apt_pkgs[a])
    else:
        print(usage)

