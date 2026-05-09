#!/bin/zsh

# Show only on new window/tab
[[ $SHLVL -gt 1 ]] && return
[[ -n "$MATT_GREETING_SHOWN" ]] && return
export MATT_GREETING_SHOWN=1

# Rainbow animated MATT banner
figlet -f chunky "MATT" | lolcat -f -a -d 2

# Typewriter "hey matt 👋"
_typewriter() {
  local msg="$1"
  for (( i=1; i<=${#msg}; i++ )); do
    printf "${msg[i]}"
    sleep 0.01
  done
  echo ""
}

_typewriter "  🦀 time to ship."
