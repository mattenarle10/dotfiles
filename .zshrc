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
plugins=(git)
source $ZSH/oh-my-zsh.sh

# Load PATHs
[ -f ~/.zsh_paths ] && source ~/.zsh_paths

# Load aliases (override Oh My Zsh plugin aliases like gl)
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

# Prompt (fallback if Powerlevel10k not loaded)
PROMPT='%F{cyan}Matt%f %F{blue}%~%f %# '

#zsh stuff
[ -f "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ] && source "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
source /opt/homebrew/share/powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
