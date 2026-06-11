# Matt's Codex Defaults

Use this file as the default working style for Codex sessions under this home directory.

## Working Style

- Read the repo before changing files. Prefer `rg`, `rg --files`, `git status`, and nearby examples before deciding.
- Keep changes scoped to the user's request. Do not refactor unrelated code or touch unrelated files.
- Work with existing patterns, frameworks, naming, formatting, and project structure.
- If a request is actionable, do the work instead of only explaining the plan.
- Before editing, briefly say what will change and why.
- After editing, run the most relevant check available: tests, typecheck, lint, build, or a targeted command.
- If a check cannot run, say exactly why.
- Protect user work. Never revert or overwrite changes you did not make unless explicitly asked.

## Communication

- Be direct, casual, and practical.
- Keep updates short while working.
- For reviews, findings come first with file and line references.
- For finished work, summarize what changed and what was verified.
- Do not over-explain simple changes.

## Coding Preferences

- Prefer small, readable changes over clever abstractions.
- Add abstractions only when they remove real duplication or match the repo's established style.
- Use structured parsers/APIs when available instead of fragile string manipulation.
- Add comments only when they clarify non-obvious logic.
- Keep generated text and code mostly ASCII unless the file already uses Unicode or the task needs it.

## Frontend Preferences

- Build the actual usable screen first, not a landing page, unless the user asks for marketing copy.
- Match the existing design system before introducing new visual ideas.
- Keep app UIs dense, useful, and easy to scan.
- Use real controls: icons for tools, tabs for views, toggles for binary options, inputs/sliders for numbers.
- Avoid decorative gradient blobs/orbs and one-note color palettes.
- Check mobile and desktop layout when doing meaningful UI work.

## Codex Workflow

- Treat Codex as a repo operator, not just a chat assistant.
- Good default prompt shape:

```text
Read the repo first. Keep the change scoped. Make the edit, run the relevant check, and summarize what changed.
```

- Prefer completing tasks end to end in one pass when feasible.
- Use project-level `AGENTS.md` files to override or add repo-specific commands, gotchas, and conventions.
