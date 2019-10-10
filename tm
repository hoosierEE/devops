#!/bin/bash

# start emacs server if not already running
export ALTERNATE_EDITOR=""
[ -z "$(ps aux | grep emacs | grep -v grep)" ] && emacs --daemon

# only prompt for keys once, at tmux start
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval `ssh-agent`
    ssh-add
fi

TMUX_NAME="lx"
tmux new-session -d -s "$TMUX_NAME" -n "develop"
tmux attach -t "$TMUX_NAME"
