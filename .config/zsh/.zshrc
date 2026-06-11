# Enable Powerlevel11k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# -------------------------------
# Matt's Zsh Configs
# -------------------------------

export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME=""
plugins=(git history-substring-search)
source $ZSH/oh-my-zsh.sh

# Vim-style command editing, with familiar shell shortcuts kept.
bindkey -v
export KEYTIMEOUT=1
bindkey '^A' beginning-of-line
bindkey '^E' end-of-line

# Search history by the command prefix already typed.
if (( $+widgets[history-substring-search-up] )); then
  bindkey '^[[A' history-substring-search-up
  bindkey '^[[B' history-substring-search-down
  bindkey -M viins '^[[A' history-substring-search-up
  bindkey -M viins '^[[B' history-substring-search-down
  bindkey -M vicmd 'k' history-substring-search-up
  bindkey -M vicmd 'j' history-substring-search-down
fi

# Load PATHs
[ -f ~/.config/zsh/.zsh_paths ] && source ~/.config/zsh/.zsh_paths

# zoxide (smarter directory jumping)
if command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init zsh)"
fi

# Load aliases (override Oh My Zsh plugin aliases like gl)
[ -f ~/.config/zsh/.zsh_aliases ] && source ~/.config/zsh/.zsh_aliases

# Load functions
[ -f ~/.config/zsh/.zsh_functions ] && source ~/.config/zsh/.zsh_functions

# Banner / greeting
[ -f ~/.config/zsh/.matt_greeting.sh ] && source ~/.config/zsh/.matt_greeting.sh

# Matt's terminal options
setopt autocd               # Just type folder name to cd
setopt correct              # Correct small typos in commands
setopt sharehistory         # Share history across tabs
setopt interactivecomments  # Allow comments in terminal

# History tuning
export HISTSIZE=1000000
export SAVEHIST=1000000
setopt HIST_IGNORE_ALL_DUPS   # no duplicate history entries
setopt HIST_FIND_NO_DUPS      # don't show duplicates when searching history
setopt HIST_REDUCE_BLANKS     # trim extra blanks in commands
setopt HIST_IGNORE_SPACE      # don't save commands prefixed with a space
setopt INC_APPEND_HISTORY     # write commands as they run, not only on shell exit

# Completion tuning.
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'

# Prompt (fallback if Powerlevel10k not loaded)
PROMPT='%F{cyan}Matt%f %F{blue}%~%f %# '

# fzf shell integration (ctrl+r = fuzzy history, ctrl+t = fuzzy file search)
[ -f "$HOMEBREW_PREFIX/opt/fzf/shell/key-bindings.zsh" ] && source "$HOMEBREW_PREFIX/opt/fzf/shell/key-bindings.zsh"
[ -f "$HOMEBREW_PREFIX/opt/fzf/shell/completion.zsh" ] && source "$HOMEBREW_PREFIX/opt/fzf/shell/completion.zsh"
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'

#zsh stuff
[ -f "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ] && source "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
[ -f "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ] && source "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
source "${HOMEBREW_PREFIX}/share/powerlevel10k/powerlevel10k.zsh-theme"

# To customize prompt, run `p10k configure` or edit ~/.config/zsh/p10k.zsh.
[[ ! -f ~/.config/zsh/p10k.zsh ]] || source ~/.config/zsh/p10k.zsh

# opencode
[ -d "$HOME/.opencode/bin" ] && export PATH="$HOME/.opencode/bin:$PATH"
