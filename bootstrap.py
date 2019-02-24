from platform import machine
import subprocess
import sys

update = 'sudo apt-get update '
apt    = 'sudo apt-get install -y '
git    = 'git clone '
gitrec = 'git clone --recursive '
curl   = 'curl -O '
jver   = 'j807_{}64.deb'.format(['amd','arm'][machine()=='aarch64'])
dpkg   = 'sudo dpkg -i '
pip3   = 'pip3 install --user '
TARGETS = {
    'emacs': [
        apt + 'emacs25-nox unifont',
    ],
    'xinu': [
        apt + 'qemu gawk bison flex libz-dev gcc-arm-none-eabi make',
        gitrec + 'git@github.iu.edu:ashroyer/xinu-s19.git ~/repo/xinu-s19',
    ],
    'k': [
        apt + 'rlwrap make',
        git + 'git@github.com:kevinlawler/kona.git $HOME/repo/kona',
        'cd $HOME/repo/kona && make && cd -',
        'rm -f $HOME/bin/k',
        'ln -s $HOME/repo/kona/k $HOME/bin/k'
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
Usage: python3 {} <options> [--dry-run]
Possible options:

{}'''.format(sys.argv[0], ''.join(
    ['{}: {}{}\n'
     .format(k, ' '*(LONGEST-len(k)), ('\n  '+' '*LONGEST).join(TARGETS[k]))
    for k in TARGETS]))

def shell(x):
    subprocess.run([x], shell=True)

if __name__ == "__main__":
    if not sum([int(a in ARGS) for a in TARGETS]): print(USAGE); exit()

    targets = [[update, 'mkdir -p $HOME/bin']]
    for a in TARGETS:
        if a in ARGS:
            targets.append(TARGETS[a])

    DRY = '--dry-run' in ARGS
    if DRY: print('  [omit --dry-run to perform the following commands]')

    for tar in targets:
        for cmd in tar:
            [shell, print][DRY](cmd)
