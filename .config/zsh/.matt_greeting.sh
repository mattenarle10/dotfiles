#!/bin/zsh

# Show greeting only once per shell session
if [[ -n "$MATT_GREETING_SHOWN" ]]; then
  return
fi
export MATT_GREETING_SHOWN=1

# Animated rainbow MATT banner
figlet -f chunky "MATT" | lolcat -a -d 1

# fastfetch system info
fastfetch --logo none \
  --structure "Title:Separator:OS:Host:Kernel:Uptime:Shell:Terminal:CPU:Memory:LocalIP" \
  --separator " → "

echo ""
