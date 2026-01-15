---
description: Create or update a Claude Code slash command (Markdown file)
argument-hint: "[command-name] (optional)"
---

# Command Creator

Create or update a Markdown-based slash command file with correct frontmatter, argument placeholders, and (optional) bash pre-execution via `!` lines.

## Slash commands: quick reference

Claude Code supports built-in slash commands (like `/help`, `/config`, `/todos`) and **custom slash commands** defined by Markdown files.

- **Built-in commands**: Provided by Claude Code itself (see official docs for the full list).
- **Custom commands**: Markdown files Claude Code can run as a prompt template.

Official docs: https://docs.claude.com/en/docs/claude-code/slash-commands

### How custom commands are discovered

Claude Code typically loads custom commands from:

- **Project commands** (shared via repo): `.claude/commands/`
- **Personal commands** (available everywhere): `~/.claude/commands/`

This repository keeps command sources under `commands/` for organization. If your Claude Code setup expects `.claude/commands/`, sync/copy the generated command file there.

### Syntax

`/<command-name> [arguments]`

- `<command-name>` is derived from the filename (without `.md`).
- Subdirectories provide **namespacing** in `/help` descriptions, but do **not** change the command name.

### Namespacing rules (important)

- `.claude/commands/frontend/test.md` and `.claude/commands/backend/test.md` both create `/test`.
- The subdirectory shows up as a qualifier in `/help` (e.g. `(project:frontend)`), so you can keep multiple commands with the same filename.
- If a project and user command share a name, the **project** one takes precedence.

### Arguments

Use placeholders inside the Markdown body:

- `$ARGUMENTS`: captures the full raw argument string.
- `$1`, `$2`, ...: positional arguments when roles matter.

Examples:

- `/fix-issue 123 high-priority` → `$ARGUMENTS` becomes `"123 high-priority"`.
- `/review-pr 456 high alice` → `$1="456"`, `$2="high"`, `$3="alice"`.

### Bash command execution (`!`)

Prefix a line with `!` to run a bash command before the prompt executes; its output is included in context.

If you use any `!` lines, add `allowed-tools` in frontmatter to permit the specific bash commands you intend to run.

Recommended style in this repo: use standalone lines that begin with `!` under a `## Context` heading.

### File references (`@`)

You can include file contents by referencing paths with `@`, e.g. `@src/index.ts` or `@README.md`.

### Frontmatter fields you’ll commonly use

- `description` (recommended/required for best UX): short, one-line summary shown in `/help`.
- `argument-hint` (recommended): a hint string shown in autocomplete.
- `allowed-tools` (required if you use `!` bash execution): list of allowed tools.
- Optional advanced fields: `context: fork`, `agent`, `model`, `disable-model-invocation`, `hooks`.

## First, ask (keep it short)

1. **Command name**: what should the user type? (Filename becomes `/<command-name>`)
2. **One-line description**: shown in `/help` and required for programmatic invocation.
3. **Arguments**: do we need all args (`$ARGUMENTS`) or positional (`$1`, `$2`, ...)?
4. **Bash context**: should the command run any `!` bash snippets? If yes, list the exact commands and add `allowed-tools: Bash(...)`.
5. **Where to place it in this repo**: pick a subdirectory under `commands/` for namespacing (directory affects description only, not the command name).

If the user doesn’t have a clear spec, propose 2-3 options and ask them to choose.

## Output requirements

Create/update a file at `commands/<namespace>/<command-name>.md` with:

1. **YAML frontmatter** (top of file) containing:
   - `description` (required)
   - `argument-hint` (recommended)
   - `allowed-tools` (required if using `!` bash execution)

2. A concise body using this structure:
   - `## Context` (optional) with `!` commands (only if needed)
   - `## Your task` describing exactly what Claude should do
   - `## Output` describing what the user will get

## Minimal template

```markdown
---
description: <one line>
argument-hint: "[args]"
allowed-tools:
  - Bash(<cmd>:*)
  - Bash(<cmd>:*)
---

## Context
!git status

## Your task
Do the thing using: $ARGUMENTS

## Output
- Summary of actions taken
- Files changed (if any)
```

Use `$ARGUMENTS` when you just need “the rest of the user input”. Use `$1`, `$2`, etc. when argument roles matter.

Avoid custom XML-like tag blocks. Use plain Markdown headings and lists instead.