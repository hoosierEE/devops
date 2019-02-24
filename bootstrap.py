# $ python3 devops.py
from platform import machine as mach
import subprocess as s
import sys

update = 'sudo apt-get update '
apt    = 'sudo apt-get install -y '
git    = 'git clone '
gitrec = 'git clone --recursive '
curl   = 'curl -O '
jver   = 'j807_{}64.deb'.format(['amd','arm'][mach()=='aarch64'])
dpkg   = 'sudo dpkg -i '
pip3   = 'pip3 install --user '

TARGETS = {
    'emacs': [
        apt + 'emacs25-nox unifont',
    ],
    'xinu': [
        apt + 'qemu gawk bison flex libz-dev gcc-arm-none-eabi make',
        gitrec + 'git@github.iu.edu:ashroyer/xinu-s19.git',
    ],
    'k': [
        git + 'git@github.com:kevinlawler/kona.git',
        'cd kona && make && cd -',
    ],
    'j': [
        curl + 'http://www.jsoftware.com/download/j807/install/' + jver,
        dpkg + jver,
        'ln -s $(which ijconsole) $HOME/bin/j',
        'rm ' + jver,
    ],
    'e110': [
        apt + 'python3-pip',
        'pip3 install --user myhdl',
    ],
}

LONGEST = max(map(len, TARGETS))
ARGS = sys.argv[1:]
USAGE = '''
Usage: python3 {} <options>
Possible options:

{}'''.format(sys.argv[0], ''.join(
    ['{}: {}{}\n'
     .format(k, ' '*(LONGEST-len(k)),
             ('\n  '+' '*LONGEST).join(TARGETS[k])
     )
             for k in TARGETS]))
def shell(cmd): s.run([cmd], shell=True)

if __name__ == "__main__":
    if not sum([int(a in ARGS) for a in TARGETS]):
        print(USAGE)
        exit()

    targets = []
    # shell(update)
    # shell('mkdir -p $HOME/bin')
    for a in TARGETS:
        if a in ARGS:
            targets.append(TARGETS[a])
    for target in targets:
        for cmd in target:
            [shell, print]['--dry-run' in ARGS](cmd)
