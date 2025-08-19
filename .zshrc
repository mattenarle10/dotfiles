# -------------------------------
# Matt's Zsh Configs
# -------------------------------

# Load PATHs
[ -f ~/.zsh_paths ] && source ~/.zsh_paths

# Load aliases
[ -f ~/.zsh_aliases ] && source ~/.zsh_aliases

# Load functions
[ -f ~/.zsh_functions ] && source ~/.zsh_functions

# Banner / greeting
[ -f ~/.matt_greeting.sh ] && source ~/.matt_greeting.sh

# Matt's terminal options
setopt autocd              # Just type folder name to cd
setopt correct             # Correct small typos in commands
setopt histignorealldups   # No duplicate history
setopt sharehistory        # Share history across tabs
setopt interactivecomments # Allow comments in terminal

# Completion system
autoload -Uz compinit
compinit

# Prompt (Starship if installed, fallback otherwise)
if command -v starship &> /dev/null; then
  eval "$(starship init zsh)"
else
  PROMPT='%F{cyan}Matt%f %F{blue}%~%f %# '
fi

