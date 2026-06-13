# Dotfiles Agent Instructions

This repository manages Matt's local shell, editor, Claude, and Codex setup.

## Scope

- Global Codex working rules live in `.codex/AGENTS.md` and should be stowed to `~/.codex/AGENTS.md`.
- Codex settings live in `.codex/config.toml`, which is stowed to `~/.codex/config.toml`.
- Keep this root file focused on dotfiles repository maintenance, not general agent behavior.

## Safety

- Never add secrets, tokens, credentials, private keys, cookies, or local-only auth files to this repo.
- Treat `.config/zsh/.zsh_secrets`, `.claude/settings.local.json`, logs, caches, histories, SQLite state, and generated runtime files as local-only.
- Do not overwrite user-local Codex state such as `~/.codex/auth.json`, sessions, logs, memories, plugin caches, or rules unless explicitly asked.
- Be careful with `~/.codex/rules/default.rules`; it changes command approval behavior globally.

## Editing

- Keep changes scoped to the requested setup area.
- Prefer updating tracked dotfiles instead of editing generated files in `~/.codex`, `~/.claude`, or `~/.config` directly.
- When adding a new stowed Codex file, update `README.md` so the expected symlink is documented.
- Preserve existing formatting style: concise Markdown, simple TOML, and shell scripts that pass `bash -n`.

## Verification

- After changing Codex TOML, parse it with `python3 -c 'import tomllib, pathlib; tomllib.loads(pathlib.Path(".codex/config.toml").read_text())'`.
- After changing `install.sh`, run `bash -n install.sh`.
- After changing stow-managed paths, check `git status --short` and mention whether activation requires running `stow .` or creating a symlink.
