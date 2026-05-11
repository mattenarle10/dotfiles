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
  eval "$(/opt/homebrew/bin/brew shellenv)"
else
  echo "✓ Homebrew already installed"
fi

# ── 3. Brew packages ────────────────────────────────────────────────────────
echo "→ Installing brew packages..."
brew install \
  git \
  stow \
  neovim \
  ghostty \
  zoxide \
  zsh-autosuggestions \
  powerlevel10k \
  figlet \
  gh \
  awscli \
  git-delta \
  hashicorp/tap/terraform \
  tree

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

# ── 7. pnpm ─────────────────────────────────────────────────────────────────
if ! command -v pnpm &>/dev/null; then
  echo "→ Installing pnpm..."
  curl -fsSL https://get.pnpm.io/install.sh | sh -
else
  echo "✓ pnpm already installed"
fi

# ── 8. Rust ─────────────────────────────────────────────────────────────────
if ! command -v rustup &>/dev/null; then
  echo "→ Installing Rust..."
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
else
  echo "✓ Rust already installed"
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
mkdir -p "$HOME/.config/ghostty"
for conflict in \
  "$HOME/.config/ghostty/config" \
  "$HOME/.claude/settings.json" \
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
