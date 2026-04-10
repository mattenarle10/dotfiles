# Matt's Dotfiles

Personal configuration files for zsh, nvim, Claude Code, and other tools.

## What's Included

- **zsh**: Shell configuration with Oh My Zsh, Powerlevel10k, zoxide (`.config/zsh/`)
- **nvim**: Neovim configuration with LSP, Telescope, Neo-tree, and Lazygit integration (`.config/nvim/`)
- **lazygit**: Git TUI configuration (`.config/lazygit/`)
- **Claude Code**: Global settings, plugins, hooks, and instructions (`.claude/`)

**📖 New to Nvim config?** Check out [NVIM_GUIDE.md](NVIM_GUIDE.md) for a step-by-step learning path!

## Quick Start

### Prerequisites

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install stow neovim lazygit
```

### Installation

1. Clone this repository:
```bash
git clone https://github.com/mattenarle10/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
```

2. Use GNU Stow to create symlinks:
```bash
# Install all configs at once
stow .

# This creates symlinks for:
# ~/.zshrc -> ~/.dotfiles/.zshrc
# ~/.config/nvim -> ~/.dotfiles/.config/nvim
# ~/.config/lazygit -> ~/.dotfiles/.config/lazygit
# ~/.claude/settings.json -> ~/.dotfiles/.claude/settings.json
# ~/.claude/hooks/* -> ~/.dotfiles/.claude/hooks/*
# etc.
```

3. Source your zsh config:
```bash
source ~/.zshrc
```

4. Open nvim to install plugins:
```bash
nvim
```
The first time you open nvim, it will automatically install all plugins.

## Nvim Keybindings (Simple!)

### Tabs (Super Simple)
- `Space + tn` - New tab
- `Space + ]` - Next tab
- `Space + [` - Previous tab
- `Space + tc` - Close tab
- `gt` / `gT` - Next/Previous tab (vim default)

### Splits
- `Space + sv` - Split vertically
- `Space + sh` - Split horizontally
- `Ctrl + h/j/k/l` - Navigate between splits
- `Space + sx` - Close split

### File Navigation
- `Space + e` - Toggle file explorer
- `Space + ff` - Find files (fuzzy) *(includes hidden files)*
- `Space + fg` - Live grep (search text in files) *(includes hidden files)*
- `Space + fw` - Find word under cursor
- `Space + fb` - Find buffers

### Git
- `Space + gg` - Open LazyGit
- `Space + gb` - Switch branches (Telescope)
- `Space + gs` - Git status (Telescope)
- `Space + gc` - Git commits (Telescope)

### LSP
- `gd` - Go to definition
- `gr` - Find references
- `K` - Hover documentation
- `Space + rn` - Rename
- `Space + ca` - Code actions

### General
- `Space + w` - Save file
- `Space + q` - Quit
- `jk` - Exit insert mode

## Uninstall

To remove symlinks:
```bash
cd ~/.dotfiles
stow -D .  # Remove all symlinks
```

## Structure

```
~/.dotfiles/
├── .claude/
│   ├── CLAUDE.md          # Global instructions
│   ├── RTK.md             # RTK token optimizer config
│   ├── settings.json      # Plugins, hooks, effort level
│   ├── settings.local.json# Local permissions
│   └── hooks/
│       └── rtk-rewrite.sh # RTK bash command rewriter
├── .config/
│   ├── nvim/              # Neovim configuration
│   │   ├── init.lua
│   │   └── lua/
│   │       ├── config/
│   │       └── plugins/
│   ├── lazygit/           # Lazygit configuration
│   │   └── config.yml
│   └── zsh/               # Zsh configuration
│       ├── .zshrc
│       ├── .zsh_aliases
│       ├── .zsh_functions
│       ├── .zsh_paths
│       ├── .matt_greeting.sh
│       └── p10k.zsh
├── .gitignore
├── NVIM_GUIDE.md          # Learn your nvim config!
└── README.md
```

