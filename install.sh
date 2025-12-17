#!/bin/bash

# Matt's Dotfiles Installation Script

set -e

echo "🚀 Installing Matt's Dotfiles..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew found"
fi

# Install required tools
echo "📦 Installing required tools..."
brew install stow neovim lazygit

# Create backup directory
BACKUP_DIR="$HOME/.dotfiles_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup existing configs
echo "💾 Backing up existing configs to $BACKUP_DIR..."
[ -f "$HOME/.zshrc" ] && mv "$HOME/.zshrc" "$BACKUP_DIR/"
[ -d "$HOME/.config/nvim" ] && mv "$HOME/.config/nvim" "$BACKUP_DIR/"
[ -d "$HOME/.config/lazygit" ] && mv "$HOME/.config/lazygit" "$BACKUP_DIR/"

# Stow configs
echo "🔗 Creating symlinks with GNU Stow..."
cd ~/.dotfiles
stow .

echo ""
echo "✨ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: source ~/.zshrc"
echo "2. Open nvim to install plugins: nvim"
echo "3. Check out the README for keybindings: cat ~/.dotfiles/README.md"
echo ""
echo "Backup of your old configs: $BACKUP_DIR"
