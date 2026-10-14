# Matt's Dotfiles

Personal configuration files for zsh, nvim, Claude Code, Codex, and other tools.

## What's Included

- **zsh**: Shell configuration with Oh My Zsh, Powerlevel10k, zoxide (`.config/zsh/`)
- **nvim**: LSP, Telescope, Neo-tree, conform.nvim formatter, Harpoon, lazygit integration (`.config/nvim/`)
- **lazygit**: Git TUI config — actually running [`lazygitrs`](https://github.com/Blankeos/lazygitrs) (Rust fork by Blankeos) behind a `~/.local/bin/lazygit` wrapper. Faster startup, AI commit generation, nicer diffs. `install.sh` now trusts the package postinstall so the real binary is downloaded, while the UI still reads the shared config file (`.config/lazygit/config.yml`)
- **ghostty**: Terminal emulator — transparency, blur, font, keybinds, tab behavior (`.config/ghostty/`)
- **Zed**: Fast GUI editor with Vim mode and Codex ACP (`.config/zed/settings.json`)
- **Claude Code**: Global settings, plugins (expo, vercel, playwright, context7, etc.), RTK hook, Caveman + ADHD response guidance, local prose-checking skill, and instructions (`.claude/`, `.agents/skills/`)
- **Codex**: Global defaults, RTK command output, Caveman + ADHD response guidance, local prose-checking skill, trusted project paths, OpenAI docs MCP, and GitHub plugin settings (`.codex/`, `.agents/skills/`)

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
- RTK for Claude command rewriting and Codex command output
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
# ~/.claude/CLAUDE.md -> ~/.dotfiles/.claude/CLAUDE.md
# ~/.claude/RTK.md -> ~/.dotfiles/.claude/RTK.md
# ~/.claude/settings.json -> ~/.dotfiles/.claude/settings.json
# ~/.claude/hooks/* -> ~/.dotfiles/.claude/hooks/*
# ~/.claude/skills/caveman -> ~/.dotfiles/.claude/skills/caveman      # -> .agents/skills/caveman
# ~/.claude/skills/i-have-adhd -> ~/.dotfiles/.claude/skills/i-have-adhd  # -> .agents/skills/i-have-adhd
# ~/.codex/config.toml -> ~/.dotfiles/.codex/config.toml
# ~/.codex/AGENTS.md -> ~/.dotfiles/.codex/AGENTS.md
# ~/.codex/fast.config.toml -> ~/.dotfiles/.codex/fast.config.toml
# ~/.codex/deep-review.config.toml -> ~/.dotfiles/.codex/deep-review.config.toml
# ~/.codex/bedrock.config.toml -> ~/.dotfiles/.codex/bedrock.config.toml
# ~/.agents/skills/caveman -> ~/.dotfiles/.agents/skills/caveman
# ~/.agents/skills/i-have-adhd -> ~/.dotfiles/.agents/skills/i-have-adhd
# ~/.agents/skills/check-prose -> ~/.dotfiles/.agents/skills/check-prose
# ~/.claude/skills/check-prose -> ~/.dotfiles/.claude/skills/check-prose  # -> .agents/skills/check-prose
# ~/AGENTS.md -> ~/.dotfiles/AGENTS.md  # dotfiles-repo guidance only
# etc.
```

To start Codex with GPT-5.6 Sol on Amazon Bedrock from this repo, run
`codex --profile bedrock -m openai.gpt-5.6-sol -c 'service_tier="default"'`.
The explicit model and tier overrides are needed here because this repo's
`.codex/config.toml` takes precedence over user-level profiles.

### Codex Response Defaults And Skills

`~/.codex/AGENTS.md` loads concise Caveman-style prose and ADHD-friendly steps
in every new Codex session. RTK reduces shell output independently. Full
explanations, exact technical details, and required safety checks take priority
over brevity. This setup uses instruction-only skills, with no Caveman proxy,
session hooks, or telemetry runtime.

The two skills are vendored from reviewed upstream revisions:

| Skill | Source | Pinned commit | Licence |
| --- | --- | --- | --- |
| `caveman` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `2e08b9177c07bb7249a8a2d1a6758e5db281d002` | Apache-2.0; upstream MIT notice retained |
| `i-have-adhd` | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | `723af7d9afaf43eb871dbcce6129e2bf80de90d5` | MIT |

Codex discovers [global skills](https://learn.chatgpt.com/docs/build-skills)
under `~/.agents/skills` and supports symlinked skill folders. The compact
global rules are always loaded; the full skill files are loaded only when
explicitly invoked with `$caveman` or `$i-have-adhd` (also available in
`/skills`). This avoids loading both complete rulesets for every task.

Say `stop caveman` to relax terse prose, `stop adhd mode` to relax structured
presentation, or `normal mode` to relax both for the current session. Invoking
a skill re-enables its style. New sessions restore the combined defaults.

On this Mac, the global `AGENTS.md` is already linked. Full `stow .` currently
has unrelated target conflicts. Activate only missing skill links with:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.dotfiles/.agents/skills/caveman ~/.agents/skills/caveman
ln -s ~/.dotfiles/.agents/skills/i-have-adhd ~/.agents/skills/i-have-adhd
```

These commands intentionally fail if a target already exists; inspect it
instead of replacing it. Do not use `stow --adopt` to resolve the conflicts.
Restart Codex to load updated global instructions; skills normally refresh
automatically. Upstream snapshots, licences, and local adaptation notes stay
with each skill. Review updates before changing the pinned revisions.

### Claude Response Defaults And Skills

`~/.claude/CLAUDE.md` gives Claude Code the same compact Caveman + ADHD
defaults in every new session and imports `RTK.md`. The rules mirror the
response-style section of `.codex/AGENTS.md`; update both when either changes.
This setup is instruction-only, with no Caveman proxy, extra hooks, or
telemetry runtime.

Claude Code's documented [skill locations](https://code.claude.com/docs/en/skills)
do not include `~/.agents/skills`, and `agents/openai.yaml` is Codex-only.
Claude discovers personal skills under `~/.claude/skills/<name>/SKILL.md`, and
a skill folder there may be a symlink. `.claude/skills/caveman` and
`.claude/skills/i-have-adhd` are tracked relative symlinks to the vendored
folders in `.agents/skills/`, so both tools share one source.
`disable-model-invocation: true` in each `SKILL.md` keeps the skill
explicit-only in Claude: its description stays out of context, and the full
text loads only when you run `/caveman` or `/i-have-adhd`.

The style controls match Codex. Say `stop caveman`, `stop adhd mode`, or
`normal mode` to relax a style for the current session. Say `caveman mode` or
`adhd mode`, or run the skill, to re-enable it. New sessions restore the
defaults. An override given in conversation is kept across compaction on a
best-effort basis, because Claude Code summarizes conversation history.

RTK for Claude keeps one native `PreToolUse` Bash hook (`rtk hook claude`) in
`.claude/settings.json`, plus the `@RTK.md` import in `CLAUDE.md`. A separate
compatibility guard runs `python3 "$HOME/.claude/hooks/rtk-safe.py"`. It rejects
misplaced leading `rtk` / `rtk proxy` prefixes on `open`, `osascript`, `pbcopy`,
and `pbpaste` (including `/usr/bin/` spellings), then tells Claude to retry
the raw command with the original arguments and approvals. Raw unsupported
commands pass through. The guard never executes, rewrites, or auto-approves
the requested command; only the native hook does supported RTK rewrites.
This avoids competing `updatedInput` results from parallel hooks. Keep one
native RTK hook and one compatibility guard; `rtk init --show` recognizes the
native hook. Compatibility instructions live in `CLAUDE.md`, because
`rtk init -g` regenerates `RTK.md`.

Codex uses global instructions, not this Claude hook: supported commands use
RTK, while unsupported and macOS utility commands run directly. `rtk proxy`
remains available for recovering output, but is not mandatory.

Verify the guard without opening apps or executing the sample commands:

```bash
rtk proxy python3 -B .claude/hooks/tests/test_rtk_safe.py
```

On this Mac, `~/.claude/CLAUDE.md`, `RTK.md`, `settings.json`, and `hooks` are
already linked. Activate only missing skill links with:

```bash
mkdir -p ~/.claude/skills
ln -s ../../.dotfiles/.claude/skills/caveman ~/.claude/skills/caveman
ln -s ../../.dotfiles/.claude/skills/i-have-adhd ~/.claude/skills/i-have-adhd
```

These relative targets match what `stow .` creates. The commands intentionally
fail if a target already exists; inspect it instead of replacing it.

Reload after changes:

- `CLAUDE.md` and `RTK.md` load at launch. Start a new Claude Code session to
  pick up edits, then check the loaded files with `/memory`.
- Skill edits apply within the running session. Run `/reload-skills` if
  `~/.claude/skills` did not exist when the session started.
- Hook edits in `settings.json` are picked up automatically. Review them with
  `/hooks`.

### AI English Checker

The shared `check-prose` skill integrates
[dlord/ai-english-checker](https://github.com/dlord/ai-english-checker), pinned at
`4eb517b42f03d2cfedded6d3a1fa8e425e991cf1`. Its unmodified source, tests,
requirements, and GPL-3.0 licence are in `.agents/skills/check-prose/vendor/`.
Both agents can select it for a prose-checking request. Invoke it directly with
`$check-prose` in Codex or `/check-prose` in Claude Code.

This is an on-request check, not a reply-blocking hook. RTK, Caveman, ADHD,
model settings, and existing hooks are unchanged. Findings are advisory, not
proof of AI authorship. Checking does not edit files; ask explicitly for a
rewrite. Rewrites stop after three passes or sooner if accuracy is at risk.

Activate only missing links; these commands fail rather than replace targets:

```bash
ln -s ~/.dotfiles/.agents/skills/check-prose ~/.agents/skills/check-prose
ln -s ../../.dotfiles/.claude/skills/check-prose ~/.claude/skills/check-prose
bash ~/.agents/skills/check-prose/scripts/install.sh
```

The installer needs `uv` and downloads Python 3.13 if necessary, pinned Python
dependencies, the spaCy English model, and NLTK WordNet. Runtime files live in
`${XDG_DATA_HOME:-$HOME/.local/share}/ai-english-checker`, not in Git or stowed
config. Ordinary checks run locally without sending prose to an external API.

Check a document directly from any directory:

```bash
rtk proxy bash ~/.agents/skills/check-prose/scripts/check-prose.sh notes.md
```

Exit `0` means no findings, `1` means findings, and `2` means an error.
For source comments/docstrings, pass `--path file.py file.py`. Standard input
checks only lines with final sentence punctuation; use a document file to
check a complete draft. Codex normally refreshes skills automatically; restart
either agent if the new skill is not listed. Review upstream changes before
updating the snapshot or rerunning installation with new requirements.

Launcher regression checks (after installation):

```bash
rtk proxy python3 -B .agents/skills/check-prose/tests/test_launcher.py
```

Our launcher uses strict UTF-8 for piped text so malformed input returns an
error instead of a misleading clean result. The upstream checker remains
unmodified. Its README examples are illustrative; use the actual findings
rather than depending on an example's exact rule wording.

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
├── .agents/
│   └── skills/            # Vendored skills shared by Codex and Claude
│       ├── caveman/
│       └── i-have-adhd/
├── .claude/
│   ├── CLAUDE.md          # Global instructions and response-style defaults
│   ├── RTK.md             # RTK token optimizer config
│   ├── settings.json      # Plugins, hooks (RTK runs as `rtk hook claude`), effort level
│   ├── settings.local.json# Local permissions (ignored)
│   ├── hooks/             # Local hook scripts
│   └── skills/            # Symlinks to ../../.agents/skills/*
├── .codex/
│   ├── AGENTS.md          # Global Codex working instructions
│   ├── config.toml        # Global Codex settings and trusted project paths
│   ├── fast.config.toml   # Fast/lower-token Codex profile
│   ├── deep-review.config.toml # Higher-effort review profile
│   └── bedrock.config.toml # Opt-in GPT-5.6 Sol on Amazon Bedrock
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
├── AGENTS.md              # Dotfiles repository instructions
├── NVIM_GUIDE.md          # Learn your nvim config!
└── README.md
```
