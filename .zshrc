# Matt's Zsh Configuration
# This file sources the main config from .config/zsh/.zshrc

if [[ -f ~/.config/zsh/.zshrc ]]; then
  source ~/.config/zsh/.zshrc
fi

alias claude-mem='bun "$HOME/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-service.cjs"'
alias nf='fastfetch'
export PATH="$HOME/.maestro/bin/maestro/bin:$PATH"
if command -v rbenv >/dev/null 2>&1; then
  eval "$(rbenv init - zsh)"
fi
export PATH="/opt/homebrew/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.terragrunt/bin:$PATH"

# opencode
export PATH=/Users/mattenarle/.opencode/bin:$PATH

# bun completions
[ -s "/Users/mattenarle/.bun/_bun" ] && source "/Users/mattenarle/.bun/_bun"

__ghostty_fastfetch_once() {
  [[ -o interactive ]] || return
  [[ "${TERM_PROGRAM:l}" == "ghostty" || "$TERM" == "xterm-ghostty" ]] || return
  command -v fastfetch >/dev/null 2>&1 || return

  local marker_dir marker
  marker_dir="$HOME/.cache/ghostty-fastfetch"
  marker="$marker_dir/shown"
  mkdir -p "$marker_dir" 2>/dev/null || return
  [[ -e "$marker" ]] && return

  : >| "$marker" 2>/dev/null || return
  fastfetch
  print
}

__ghostty_fastfetch_once
unfunction __ghostty_fastfetch_once
export PATH="$HOME/.local/bin:$PATH"
