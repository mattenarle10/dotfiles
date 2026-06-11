#!/usr/bin/env bash
set -e

echo "🚀 Matt's Mac Setup"
echo "==================="

# ── 1. Xcode CLI Tools ──────────────────────────────────────────────────────
if ! xcode-select -p &>/dev/null; then
  echo "→ Installing Xcode CLI tools..."
  xcode-select --install
  echo "  Waiting for Xcode tools to finish before continuing..."
  until xcode-select -p &>/dev/null; do sleep 5; done
else
  echo "✓ Xcode CLI tools already installed"
fi

# ── 2. Homebrew ─────────────────────────────────────────────────────────────
if ! command -v brew &>/dev/null; then
  echo "→ Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "✓ Homebrew already installed"
fi

if command -v brew &>/dev/null; then
  eval "$(brew shellenv)"
elif [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
  eval "$(/usr/local/bin/brew shellenv)"
else
  echo "✗ Homebrew install failed or brew is not on a known path"
  exit 1
fi

# ── 3. Brew packages ────────────────────────────────────────────────────────
echo "→ Installing brew packages..."
brew install \
  git \
  jq \
  stow \
  neovim \
  ghostty \
  bat \
  eza \
  fd \
  fzf \
  ripgrep \
  zoxide \
  zsh-autosuggestions \
  zsh-syntax-highlighting \
  powerlevel10k \
  figlet \
  lolcat \
  gh \
  awscli \
  git-delta \
  hashicorp/tap/terraform \
  firebase-cli \
  poppler \
  openjdk@21 \
  jmeter \
  rbenv \
  ruby \
  fastfetch \
  helm \
  tree

# GUI apps managed by Homebrew casks.
if [ ! -d "/Applications/Zed.app" ]; then
  echo "→ Installing Zed..."
  brew install --cask zed
else
  echo "✓ Zed already installed"
fi

# ── 4. Oh My Zsh ────────────────────────────────────────────────────────────
# Install BEFORE stowing — the installer always overwrites ~/.zshrc, which
# would clobber our symlink if stow ran first.
if [ ! -f "$HOME/.oh-my-zsh/oh-my-zsh.sh" ]; then
  echo "→ Installing Oh My Zsh..."
  RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  # Remove the .zshrc the installer just created so stow can place our symlink
  rm -f "$HOME/.zshrc"
else
  echo "✓ Oh My Zsh already installed"
fi

# ── 5. NVM + Node ───────────────────────────────────────────────────────────
if [ ! -d "$HOME/.nvm" ]; then
  echo "→ Installing NVM..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/HEAD/install.sh | bash
else
  echo "✓ NVM already installed"
fi

# ── 6. Bun ──────────────────────────────────────────────────────────────────
if ! command -v bun &>/dev/null; then
  echo "→ Installing Bun..."
  curl -fsSL https://bun.sh/install | bash
else
  echo "✓ Bun already installed"
fi

# ── 6a. lazygitrs (Rust fork of lazygit) ────────────────────────────────────
if ! command -v lazygitrs &>/dev/null; then
  echo "→ Installing lazygitrs..."
  bun install -g lazygitrs
fi
# Wrapper so anything calling `lazygit` (terminal, lazygit.nvim) hits lazygitrs
if [ ! -f "$HOME/.local/bin/lazygit" ]; then
  echo "→ Creating lazygit → lazygitrs wrapper..."
  mkdir -p "$HOME/.local/bin"
  cat > "$HOME/.local/bin/lazygit" <<'WRAP'
#!/usr/bin/env bash
exec lazygitrs "$@"
WRAP
  chmod +x "$HOME/.local/bin/lazygit"
fi

# Zed's direct app download does not always put the `zed` CLI on PATH.
if [ -x "/Applications/Zed.app/Contents/MacOS/cli" ] && [ ! -e "$HOME/.local/bin/zed" ]; then
  echo "→ Creating zed CLI wrapper..."
  mkdir -p "$HOME/.local/bin"
  ln -s "/Applications/Zed.app/Contents/MacOS/cli" "$HOME/.local/bin/zed"
fi

# ── 7. pnpm ─────────────────────────────────────────────────────────────────
if ! command -v pnpm &>/dev/null; then
  echo "→ Installing pnpm..."
  curl -fsSL https://get.pnpm.io/install.sh | sh -
else
  echo "✓ pnpm already installed"
fi

# ── 7a. Global npm tools (LSPs, CLIs) ───────────────────────────────────────
# Source NVM so npm is on PATH for this shell session.
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
if command -v npm &>/dev/null; then
  echo "→ Installing global npm tools (Codex, TypeScript LSP, etc)..."
  npm install -g @openai/codex typescript typescript-language-server
else
  echo "⚠ npm not found — skipping global npm tools (run 'nvm install --lts' then re-run this script)"
fi

# ── 8. Rust ─────────────────────────────────────────────────────────────────
if ! command -v rustup &>/dev/null; then
  echo "→ Installing Rust..."
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
else
  echo "✓ Rust already installed"
fi
[ -f "$HOME/.cargo/env" ] && \. "$HOME/.cargo/env"
if command -v cargo &>/dev/null && ! command -v rtk &>/dev/null; then
  echo "→ Installing RTK for Claude command rewriting..."
  cargo install rtk
fi

# ── 9. uv (Python) ──────────────────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
  echo "→ Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
else
  echo "✓ uv already installed"
fi

# ── 10. Clear stow conflicts ────────────────────────────────────────────────
# These tools/installers create default configs — remove them so stow can
# place our symlinks cleanly.
mkdir -p "$HOME/.config/ghostty" "$HOME/.config/zed" "$HOME/.codex"
for conflict in \
  "$HOME/.config/ghostty/config" \
  "$HOME/.config/zed/settings.json" \
  "$HOME/.codex/config.toml" \
  "$HOME/.claude/settings.json" \
  "$HOME/AGENTS.md" \
  "$HOME/.zshrc"
do
  if [ -f "$conflict" ] && [ ! -L "$conflict" ]; then
    echo "→ Backing up existing $conflict → ${conflict}.bak"
    mv "$conflict" "${conflict}.bak"
  fi
done

# ── 11. Stow dotfiles ───────────────────────────────────────────────────────
DOTFILES="$HOME/.dotfiles"
if [ ! -d "$DOTFILES" ]; then
  echo "→ Cloning dotfiles..."
  git clone https://github.com/mattenarle10/dotfiles.git "$DOTFILES"
fi

echo "→ Stowing dotfiles..."
cd "$DOTFILES"
stow .

echo ""
echo "✅ Done! Restart your terminal or run: source ~/.zshrc"
echo ""
echo "Next steps:"
echo "  • Open nvim — plugins install automatically on first launch"
echo "  • Run 'p10k configure' to set up your prompt if needed"
echo "  • Install Claude Code: npm install -g @anthropic-ai/claude-code"
