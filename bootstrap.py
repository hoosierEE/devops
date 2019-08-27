# basically a Dockerfile, but in Python3
# NOTE: Ubuntu only
import platform
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
JVER   = '807'  # or 807
mach   = int(platform.machine()=='aarch64')
jurl   = 'j{}_{}64.deb'.format(JVER, ['amd','arm'][mach])
jbeta  = 'http://www.jsoftware.com/download/j901/install/j901_'+['linux','raspi'][mach]+'64.tar.gz'

# strings of commands, sent (in order) to subprocess.run()
TARGETS = {
    'tmux': [
        apt + 'tmux',
    ],
    'emacs': [
        apt + 'emacs25-nox unifont',
    ],
    'emacs_org_fix': [
        'for dir in "$HOME/.emacs.d/elpa/org-"*/; do find $dir -name "*.elc" -delete; done',
    ],
    'xinu': [
        apt + 'qemu gawk bison flex libz-dev gcc-arm-none-eabi make',
        gitrec + 'git@github.iu.edu:ashroyer/xinu-s19.git ' + repodir + 'xinu-s19',
    ],
    'k': [
        apt + 'rlwrap make',
        git + 'git@github.com:kevinlawler/kona.git ' + repodir + 'kona',
        'cd ' + repodir + 'kona && make && cd -',
        'rm -f ' + bindir + 'k',
        'ln -s ' + repodir + 'kona/k ' + bindir + 'k',
    ],
    'j': [
        curl + 'http://www.jsoftware.com/download/j' + JVER + '/install/' + jurl,
        dpkg + jurl,
        'ln -s $(which ijconsole) ' + bindir + 'j',
        'rm ' + jurl,
    ],
    'jbeta': [
        curl + jbeta,
        'tar xzf j901*',
        'mv j901* ~/',
        'ln -s ~/j901/bin/jconsole ' + bindir + 'j',
        'rm ~/j901_' + ['linux','raspi'][mach] + '64.tar.gz',
        'rm -r j901',
    ],
    'myhdl': [
        apt + 'python3-pip',
        'pip3 install --user myhdl',
    ],
    'tex': [
        'wget -qO- "https://yihui.name/gh/tinytex/tools/install-unx.sh" | sh'
    ],
    # 'texlive': [
    #     apt + 'texlive-latex-recommended',
    # ]
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

