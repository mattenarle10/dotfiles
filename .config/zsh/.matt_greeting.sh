#!/bin/zsh

# Show only on new window/tab
[[ $SHLVL -gt 1 ]] && return
[[ -n "$MATT_GREETING_SHOWN" ]] && return
export MATT_GREETING_SHOWN=1

# 3D rainbow animated banner — run in subshell with TTY so lolcat -a works
figlet -f larry3d "MATT" | lolcat -f

echo "\n  🦀 time to ship.\n"
