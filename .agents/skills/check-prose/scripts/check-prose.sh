#!/usr/bin/env bash
set -euo pipefail

runtime="${XDG_DATA_HOME:-$HOME/.local/share}/ai-english-checker"
python="$runtime/venv/bin/python"
checker="$runtime/check_prose.py"

if [[ ! -x "$python" || ! -f "$checker" || ! -f "$runtime/nltk_data/corpora/wordnet.zip" ]]; then
  printf '%s\n' 'AI English Checker is not installed. Run:' \
    'bash ~/.agents/skills/check-prose/scripts/install.sh' >&2
  exit 2
fi

# Reject malformed piped text instead of silently dropping undecodable bytes.
export PYTHONIOENCODING=utf-8:strict
exec "$python" -B "$checker" "$@"
