#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/dodeca-6-tope/claude-telegram.git"

# -- Install uv if missing ----------------------------------------------------
if ! command -v uv &>/dev/null; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# -- Install claude-telegram ---------------------------------------------------
echo "Installing claude-telegram..."
uv tool install --force "git+$REPO"

echo ""
echo "Done. Set env vars and run:"
echo "  export TELEGRAM_BOT_TOKEN=..."
echo "  claude-telegram"
