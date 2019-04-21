#!/bin/bash
export ALTERNATE_EDITOR=""  # emacsclient starts server
if [ -z "$(ps aux | grep emacs | grep -v grep)" ]; then
    # start emacs server if not already running
    emacs --daemon && echo "started emacs server"
fi

tmux new-session -d -s "lx" -n "misc"
tmux send-keys "emacsclient -nw" C-m
tmux split-window -v -p 10

for i in "$@"; do
    tmux new-window -n "$i"
    tmux send-keys "emacsclient -nw" C-m
    tmux split-window -v -p 10
done

tmux attach -t "lx"
