# basically a Dockerfile, but in Python3
from platform import machine
import subprocess
import sys

# aliases for command prefixes (note trailing space)
update  = 'sudo apt-get update '
apt     = 'sudo apt-get install -y '
git     = 'git clone '
gitrec  = 'git clone --recursive '
curl    = 'curl -O '
dpkg    = 'sudo dpkg -i '
pip3    = 'pip3 install --user '
bindir  = '$HOME/bin/'
repodir = '$HOME/repo/'

# aliases for deb packages (just the one at the moment)
jver   = 'j807_{}64.deb'.format(['amd','arm'][machine()=='aarch64'])

# strings of commands, sent (in order) to subprocess.run()
TARGETS = {
    'tmux': [
        apt+'tmux',
    ],
    'emacs': [
        apt+'emacs25-nox unifont',
    ],
    'emacs_org_fix': [
        'for dir in "$HOME/.emacs.d/elpa/org-"*/; do find $dir -name "*.elc" -delete; done',
    ],
    'xinu': [
        apt+'qemu gawk bison flex libz-dev gcc-arm-none-eabi make',
        gitrec+'git@github.iu.edu:ashroyer/xinu-s19.git '+repodir+'xinu-s19',
    ],
    'k': [
        apt+'rlwrap make',
        git+'git@github.com:kevinlawler/kona.git '+repodir+'kona',
        'cd '+repodir+'kona && make && cd -',
        'rm -f '+bindir+'k',
        'ln -s '+repodir+'kona/k '+bindir+'k',
    ],
    'j': [
        curl+'http://www.jsoftware.com/download/j807/install/'+jver,
        dpkg+jver,
        'ln -s $(which ijconsole) '+bindir+'j',
        'rm '+jver,
    ],
    'e110': [
        apt+'python3-pip',
        'pip3 install --user myhdl',
    ],
    'tex': [
        'wget -qO- "https://yihui.name/gh/tinytex/tools/install-unx.sh" | sh'
    ],
    'texlive': [
        apt+'texlive-latex-recommended',
    ]
}

# print help text and nicely-formatted TARGETS
LONGEST = max(map(len, TARGETS))
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
    ARGS = sys.argv[1:]
    if not sum([int(a in ARGS) for a in TARGETS]): print(USAGE); exit()

    # add pre-requisites here if desired
    targets = [
        [update, 'mkdir -p '+bindir],
        [apt+'wget'],
    ]
    for a in TARGETS: # append targets specified on CLI
        if a in ARGS:
            targets.append(TARGETS[a])

    dry = '--dry-run' in ARGS
    if dry: print('  [omit --dry-run to perform the following commands]')
    for tar in targets: # install (or just print) everything in the list
        for cmd in tar:
            [shell, print][dry](cmd)

