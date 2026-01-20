# Matt's Zsh Configuration
# This file sources the main config from .config/zsh/.zshrc

if [[ -f ~/.config/zsh/.zshrc ]]; then
  source ~/.config/zsh/.zshrc
fi

alias claude-mem='bun "/Users/matt/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-service.cjs"'
