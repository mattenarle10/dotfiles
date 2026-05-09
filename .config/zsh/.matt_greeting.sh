#!/bin/zsh

# Show only on new window/tab
[[ $SHLVL -gt 1 ]] && return
[[ -n "$MATT_GREETING_SHOWN" ]] && return
export MATT_GREETING_SHOWN=1

echo ""
printf "  " && figlet -f larry3d "MATT" | sed 's/^/  /' | lolcat -f
echo ""
printf "  🦀 time to ship.\n\n"
