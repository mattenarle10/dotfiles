#!/bin/zsh

# Show greeting only on new window/tab (not on clear or subshells)
[[ $SHLVL -gt 1 ]] && return
[[ -n "$MATT_GREETING_SHOWN" ]] && return
export MATT_GREETING_SHOWN=1

# Rainbow MATT banner
figlet -f chunky "MATT" | lolcat -f

# fastfetch system info
fastfetch --logo none \
  --structure "Title:Separator:OS:Host:Kernel:Uptime:Shell:Terminal:CPU:Memory:LocalIP" \
  --separator " → "

echo ""
