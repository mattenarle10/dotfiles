# AI English Checker

## Can you stand AI English?

Are you tired of AI English slop? Does reading english written by AI hurt your brain? Are you pulling your hair because of the wall of text?

This simple python program can tell you everything that's wrong with a given wall of text.

## Who is this for?

For the developer trying to decipher AI English.

For the office worker spending hours reprompting to create human-sounding emails.

For the tired professor checking students' essays.

For people who have the tokens to punish AI for writing stupid English.

## How this works

This heavily relies on NLP via [spaCy](https://pypi.org/project/spacy/) to check the english grammar. It detects for the presence of patterns commonly seen in text written by AI, and reports each violation.

Most human beings may have one or two violations. But AI text will have a lot more.

## Installation

Prerequisites: python3

Make the virtualenv and install the requirements into it:

```
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

`requirements.txt` pins the spaCy model `en_core_web_md` as a wheel, so you download no model separately.

## Integrating with Claude Code

This is meant to be used either as a skill or as a hook.

### As a Stop hook

Save this script as `~/.claude/hooks/check-prose-stop.sh`. Run `chmod +x` on the file:

```bash
#!/usr/bin/env bash
set -uo pipefail

python="$HOME/Applications/ai-english-checker/venv/bin/python"
checker="$HOME/Applications/ai-english-checker/check_prose.py"

message="$(jq -r '.last_assistant_message // ""')"
[ -z "$message" ] && exit 0

findings="$(printf '%s' "$message" | "$python" "$checker")"
status=$?
[ "$status" -eq 1 ] || exit 0

printf 'Rewrite these sentences before the turn ends:\n%s\n' "$findings" >&2
exit 2
```

Then register it in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/you/.claude/hooks/check-prose-stop.sh",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

Claude Code runs a Stop hook when the main agent finishes its reply. The hook reads a JSON object on standard input. The text of that reply arrives in the field `last_assistant_message`.

The hook blocks the turn when it exits with code 2. Claude then reads the stderr text as the reason and writes the message again.

Claude Code ends the turn anyway after 8 consecutive blocks. A counter in a temp file stops the hook before that cap.

A Stop hook runs after the reply reaches the screen, so you still see the bad text. The stop hook forces a rewrite, until the hook is satisfied.

`~/.claude/settings.json` covers every project on your machine. A `.claude/settings.json` inside a repository covers that repository, and you can commit it for your team.

### As a skill

Make the directory:

```bash
mkdir -p ~/.claude/skills/check-prose
```

Save the following file as `~/.claude/skills/check-prose/SKILL.md`:

```markdown
---
description: Checks a document for AI English with the ai-english-checker. Use when the user asks to check prose, or when the user names AI English.
---

## Instructions

Run the checker on the file the user names:

`~/Applications/ai-english-checker/venv/bin/python ~/Applications/ai-english-checker/check_prose.py <file>`

Print every finding. Rewrite each sentence the checker reports. Run the command again, and repeat until it exits 0.
```

Type `/check-prose` to run it. Claude also loads a skill on its own when your request matches the description.

The hook and the skill do different jobs. The hook guards every reply Claude writes to you. The skill checks a file when you ask for it.

## How to use

### Supported Inputs

#### Standard input:

```
printf 'The docs say the flag is required.\n' | ./venv/bin/python check_prose.py
```

That text has one finding:

```
a thing cannot speak or decide: say who did it, or say what the thing is	The docs say the flag is required.
```

#### File input

```
./venv/bin/python check_prose.py notes.md
```

The following filename extensions are supported:

```
.md .markdown .txt .rst .adoc
```

#### Source code

```
./venv/bin/python check_prose.py --path check_prose.py check_prose.py
```

Pass `--path` for the comments and docstrings of a source file. The flag repeats the name of the file so the reader can pick the comment syntax for that language.

### Output

Each finding comes out on its own line. The rule opens that line. A tab separates the rule from the sentence. Exit code 0 means clean. Exit code 1 means at least one finding. Exit code 2 means the command could not read its input or could not load the model.

### Text handling

A chat message keeps only the lines that end in a period, a question mark, an exclamation mark or a colon.

A line of code ends in a brace or a comma, so the reader drops that line before the parser sees it.

A document keeps every line of prose, and the reader strips fenced code, headings, tables, list markers and bold markers first.

## How to run the tests

Run the suite from the tests directory:

```
cd tests
../venv/bin/python -m unittest test_check_prose_cli
```

Five tests drive the command in a subprocess.

Each scenario is one row in `tests/data/check_failure.csv` or in `tests/data/check_success.csv`. A row gives the text, the exit code, the count of findings and the finding text.

A row with an empty form column runs three times. The runner feeds the text on standard input. It then writes the same text into `doc.md`, and after that into a comment in `mod.py`. The command must report the same findings in all three.

A row that fills the form column runs only in the forms written in that column. Those rows pin the unwrapping of one form, for example a docstring or a line without final punctuation.

The suite keeps eight of those runs open at a time, and it finishes in about 80 seconds.
