---
name: check-prose
description: Check a named document or supplied prose for AI-style English with the local ai-english-checker. Use when Matt asks to check prose, remove AI-style wording, or use AI English Checker.
---

# Check Prose

Use the local checker for the text or file Matt names. Do not check every reply,
scan unrelated files, or interpret findings as proof that AI wrote the text.

The launcher is `~/.agents/skills/check-prose/scripts/check-prose.sh` in Codex
and `~/.claude/skills/check-prose/scripts/check-prose.sh` in Claude Code.
It works from any project directory. Prefix it with `rtk proxy` when available.

## Run

- Document: `bash <launcher> "<file>"`.
- Source comments/docstrings: `bash <launcher> --path "<file>" "<file>"`.
- Supplied prose: send the text on standard input to `bash <launcher>`.
  Standard input checks only lines ending in `.`, `?`, `!`, or `:`. For a complete
  draft, use a temporary `.md` or `.txt` file instead.
- Document extensions: `.md`, `.markdown`, `.txt`, `.rst`, `.adoc`.
- Report every finding with its sentence. Exit `0` means no findings, `1` means
  findings, and `2` means an input, dependency, or model error. Never call a
  failed check clean. If the runtime is missing, show the install command and
  ask before downloading dependencies or writing outside the workspace.

## Review And Rewrite

Treat findings as style suggestions, not grammar verdicts. Preserve meaning,
commands, code, API names, quotations, numbers, units, negations, and uncertainty.
The checker can flag valid technical wording such as "the docs say".

If Matt asks only for a check, report findings without changing the file.
If he requests a rewrite, edit only the requested prose, then check it again.
Use at most three check/rewrite passes. Stop earlier if findings repeat or a
rewrite would change technical meaning. Explain unresolved findings and ask
Matt to decide; do not chase a zero result at the expense of accuracy.

Keep Caveman/ADHD presentation and RTK independent of the checker's findings.

## Source

Adapted from the skill example in [dlord/ai-english-checker](https://github.com/dlord/ai-english-checker)
at commit `4eb517b42f03d2cfedded6d3a1fa8e425e991cf1`.
`vendor/` preserves its source, tests, requirements, README, and GPL-3.0 licence
without modifications. Local additions provide installation, invocation, and
bounded advisory review. No Stop hook, external AI service, or telemetry is added.
