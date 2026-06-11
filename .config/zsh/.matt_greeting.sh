#!/bin/zsh

matt-greeting() {
  echo ""
  figlet -f larry3d "MATT" | sed 's/^/  /' | lolcat -f
  echo ""
  printf "  time to ship.\n\n"
}

# Keep new terminals clean. Run `banner` when you want the big greeting.
if [[ "$MATT_SHOW_GREETING" == 1 && -z "$MATT_GREETING_SHOWN" && $SHLVL -le 1 ]]; then
  export MATT_GREETING_SHOWN=1
  matt-greeting
fi
