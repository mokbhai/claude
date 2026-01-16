---
description: Suggest and create Claude Code hooks for this project
argument-hint: "[hook-goal] (optional)"
---

# Hook Creator

Analyze the repo, propose practical hooks, then implement (and test) the chosen hook.

## How to run this command

Use `$ARGUMENTS` as the initial “hook goal” if provided (e.g. `"format on edit"`, `"block secrets in commits"`).

## Step 1: Quick repo scan

Inspect for common tooling and existing hook configuration (only read files unless the user agrees to changes):

- TypeScript: `tsconfig.json`, `package.json`
- Lint/format: `.eslintrc*`, `biome.json`, `.prettierrc*`, `ruff.toml`, `pyproject.toml`
- Tests: `package.json` scripts, `pytest.ini`, `go.mod`, etc.
- Existing Claude hooks: `hooks.settings.json`, `.claude/hooks/`, `~/.claude/hooks/`

## Step 2: Propose 2-5 hooks

Give a short ranked list with:

- Hook **event** (`PreToolUse`, `PostToolUse`, `Stop`, etc.)
- Tool **matcher** (`Bash`, `Write`, `Edit`, `*`, etc.)
- Whether it **blocks** (only `PreToolUse` can block)
- What it checks and how it reports findings

Examples of good defaults:

- PostToolUse: auto-suggest formatting/lint fixes for touched files
- PreToolUse (Bash): block obvious secret leaks or dangerous git commands

## Step 3: Confirm requirements (ask only what you need)

Ask targeted questions:

1. Where should it live: project (`.claude/hooks/`) or user (`~/.claude/hooks/`)?
2. Should it block operations, or only warn?
3. Which file patterns to include/exclude?
4. Should successful runs be silent (`suppressOutput`) to reduce noise?

## Step 4: Implement the hook correctly

Implementation requirements:

- Read JSON **from stdin** (not argv)
- Output the correct top-level JSON shape
- Provide actionable messages via `additionalContext` when helpful
- Keep the hook fast; prefer operating on changed files

## Step 5: Test both paths

Test:

- Happy path (no issues) — verify it stays quiet if configured
- Sad path (issue present) — verify warnings/blocking works as intended

## Reference

- Official hooks docs: https://docs.claude.com/en/docs/claude-code/hooks
