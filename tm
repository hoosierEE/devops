#!/bin/bash

# start emacs server if not already running
if [ ! $(uname) = "Darwin" ]; then
    export ALTERNATE_EDITOR=""
    if [ -z "$(ps aux | grep emacs | grep -v grep)" ]; then
        emacs --daemon
    fi
fi

# # only prompt for keys once, at tmux start
# if [ -z "$SSH_AUTH_SOCK" ]; then
#     eval `ssh-agent`
#     ssh-add
# fi

TMUX_NAME="lx"
tmux new-session -d -s "$TMUX_NAME" -n "develop"
tmux attach -t "$TMUX_NAME"
