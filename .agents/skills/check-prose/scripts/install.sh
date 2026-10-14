#!/usr/bin/env bash
set -euo pipefail

skill="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
runtime="${XDG_DATA_HOME:-$HOME/.local/share}/ai-english-checker"

if ! command -v uv >/dev/null 2>&1; then
  printf '%s\n' 'Install uv before setting up AI English Checker.' >&2
  exit 2
fi

# Keep dependencies, downloaded corpora, and test runtime outside stowed files.
mkdir -p "$runtime"
cp "$skill/vendor/check_prose.py" "$skill/vendor/phrases.txt" \
  "$skill/vendor/requirements.txt" "$skill/vendor/LICENSE" "$runtime/"
if [[ ! -x "$runtime/venv/bin/python" ]]; then
  uv venv --python 3.13 "$runtime/venv"
fi
uv pip install --python "$runtime/venv/bin/python" -r "$runtime/requirements.txt"
"$runtime/venv/bin/python" -B -c \
  'import nltk, sys; nltk.download("wordnet", download_dir=sys.argv[1], raise_on_error=True)' \
  "$runtime/nltk_data"
"$runtime/venv/bin/python" -B "$runtime/check_prose.py" </dev/null
printf '%s\n' 'AI English Checker is installed. Checks now run locally.'
