# I Have ADHD For Matt's Codex And Claude Code

Source: [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd).
Pinned revision: `723af7d9afaf43eb871dbcce6129e2bf80de90d5`.
Upstream file: `skills/i-have-adhd/SKILL.md`.
Licence: MIT; see `LICENSE` for the retained copyright and permission notice.

Local changes shorten the description, use Codex's `$i-have-adhd` invocation,
and add provenance. The rules and upstream OpenAI invocation policy are retained.
The Gemini-only command file is omitted.

Compact always-on defaults live in `~/.codex/AGENTS.md`; invoke this skill to
load the full rules. Say `stop adhd mode` or `normal mode` to stop it for the
current session. Fresh sessions restore the global defaults. Caveman brevity
must not hide a required step, uncertainty, or an explanation Matt requested.

Claude Code loads this same folder through the `~/.claude/skills/i-have-adhd`
symlink and invokes it as `/i-have-adhd`. The upstream
`disable-model-invocation: true` frontmatter keeps it explicit-only there and
keeps its description out of context. `agents/openai.yaml` applies to Codex
only. Claude's compact always-on rules live in `~/.claude/CLAUDE.md`.

Review upstream changes before updating the revision; preserve these adaptations.
