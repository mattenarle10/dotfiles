# Matt's Dotfiles

Personal configuration files for zsh, nvim, Claude Code, Codex, and other tools.

## What's Included

- **zsh**: Shell configuration with Oh My Zsh, Powerlevel10k, zoxide (`.config/zsh/`)
- **nvim**: LSP, Telescope, Neo-tree, conform.nvim formatter, Harpoon, lazygit integration (`.config/nvim/`)
- **lazygit**: Git TUI config — actually running [`lazygitrs`](https://github.com/Blankeos/lazygitrs) (Rust fork by Blankeos) behind a `~/.local/bin/lazygit` wrapper. Faster startup, AI commit generation, nicer diffs. Same config file (`.config/lazygit/config.yml`)
- **ghostty**: Terminal emulator — transparency, blur, font, keybinds, tab behavior (`.config/ghostty/`)
- **Zed**: Fast GUI editor with Vim mode and Codex ACP (`.config/zed/settings.json`)
- **Claude Code**: Global settings, plugins (expo, vercel, playwright, context7, etc.), RTK hooks, and instructions (`.claude/`)
- **Codex**: Global defaults, trusted project paths, OpenAI docs MCP, and GitHub plugin approvals (`.codex/config.toml`, `AGENTS.md`)

**📖 New to Nvim config?** Check out [NVIM_GUIDE.md](NVIM_GUIDE.md) for a step-by-step learning path!

## Quick Start (Fresh Mac)

### One-liner setup

```bash
# 1. Install Xcode CLI tools first (needed for git)
xcode-select --install

# 2. Clone dotfiles
git clone https://github.com/mattenarle10/dotfiles.git ~/.dotfiles

# 3. Run the install script — handles everything else
cd ~/.dotfiles && bash install.sh
```

The `install.sh` script automatically installs and configures:
- Homebrew
- CLI: Neovim, Ghostty, jq, bat, eza, fd, fzf, ripgrep, zoxide, zsh-autosuggestions, zsh-syntax-highlighting, Powerlevel10k, figlet/lolcat, gh, awscli, git-delta, terraform, firebase-cli, poppler, JMeter/OpenJDK 21, rbenv/Ruby, fastfetch, helm, tree
- Casks: Zed
- Oh My Zsh
- NVM (Node.js)
- Bun, pnpm
- Rust
- RTK for Claude command rewriting
- uv (Python)
- Codex CLI, TypeScript, and TypeScript language server
- lazygitrs (with `lazygit` wrapper for backward compat)
- Stows all dotfiles into place

### What stow sets up

```bash
# ~/.zshrc -> ~/.dotfiles/.zshrc
# ~/.config/nvim -> ~/.dotfiles/.config/nvim
# ~/.config/lazygit -> ~/.dotfiles/.config/lazygit
# ~/.config/ghostty/config -> ~/.dotfiles/.config/ghostty/config
# ~/.config/zed/settings.json -> ~/.dotfiles/.config/zed/settings.json
# ~/.claude/settings.json -> ~/.dotfiles/.claude/settings.json
# ~/.claude/hooks/* -> ~/.dotfiles/.claude/hooks/*
# ~/.codex/config.toml -> ~/.dotfiles/.codex/config.toml
# ~/AGENTS.md -> ~/.dotfiles/AGENTS.md
# etc.
```

### After install

```bash
source ~/.zshrc       # reload shell
nvim                  # opens nvim — plugins install automatically on first launch
p10k configure        # reconfigure prompt if needed
```

### Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### Runtime state not tracked

These stay local because they contain auth, cache, history, generated state, or machine-specific runtime data: `~/.codex/auth.json`, Codex logs/sessions/SQLite files, `~/.claude` history/cache/projects, `~/.config/gh`, `~/.config/gcloud`, `~/.config/configstore`, and local logs.

## Editor Workflow

- Use `nvim .` when you want the terminal-native setup, fast keyboard work, lazygit integration, and your full Lua config.
- Use `zed .` when you want a fast GUI editor with Vim mode, project search, previews, and Codex ACP in the editor.
- Keep shared habits the same in both: Vim motions, 2-space indentation, dark Ayu theme, and repo-level agent instructions from `AGENTS.md`.

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
- `Space + gg` - Open lazygit (lazygitrs)
- `Space + gb` - Switch branches (Telescope)
- `Space + gs` - Git status (Telescope)
- `Space + gc` - Git commits (Telescope)

### Harpoon (quick file marks)
- `Space + a` - Add current file to harpoon
- `Ctrl + e` - Toggle harpoon menu
- `Space + 1/2/3/4` - Jump to harpoon file 1-4

### Format
- `Space + f` - Format buffer (conform.nvim — auto-runs on save)

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
│   ├── settings.local.json# Local permissions (ignored)
│   └── hooks/
│       └── rtk-rewrite.sh # RTK bash command rewriter
├── .codex/
│   └── config.toml        # Global Codex defaults and trusted project paths
├── .config/
│   ├── nvim/              # Neovim configuration
│   │   ├── init.lua
│   │   └── lua/
│   │       ├── config/
│   │       └── plugins/
│   ├── lazygit/           # Lazygit configuration
│   │   └── config.yml
│   ├── ghostty/           # Ghostty terminal config
│   │   └── config
│   ├── zed/               # Zed GUI editor config
│   │   └── settings.json
│   └── zsh/               # Zsh configuration
│       ├── .zshrc
│       ├── .zsh_aliases
│       ├── .zsh_functions
│       ├── .zsh_paths
│       ├── .matt_greeting.sh
│       └── p10k.zsh
├── .gitignore
├── AGENTS.md              # Default Codex working instructions
├── NVIM_GUIDE.md          # Learn your nvim config!
└── README.md
```
