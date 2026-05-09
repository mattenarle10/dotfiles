#!/bin/zsh

# Show only on new window/tab
[[ $SHLVL -gt 1 ]] && return
[[ -n "$MATT_GREETING_SHOWN" ]] && return
export MATT_GREETING_SHOWN=1

# 3D rainbow animated banner — run in subshell with TTY so lolcat -a works
figlet -f larry3d "MATT" | lolcat -f -a -d 3 -s 50

# Typewriter effect
_typewriter() {
  local msg="$1"
  for (( i=1; i<=${#msg}; i++ )); do
    printf "${msg[i]}"
    sleep 0.02
  done
  printf "\n\n"
}

_typewriter "  🦀 time to ship."
