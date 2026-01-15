---
description: Set up Husky + lint-staged git hooks for this repository
argument-hint: "[--yes] (optional)"
allowed-tools:
  - Bash(git:*)
  - Bash(npx:*)
  - Bash(npm:*)
  - Bash(pnpm:*)
  - Bash(yarn:*)
  - Bash(bun:*)
  - Bash(cat:*)
  - Bash(ls:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - Bash(echo:*)
---

# Husky Setup

Set up Husky in a safe, repo-aware way.

## Context

!git status --porcelain=v1 || true
!test -f package.json && echo "package.json found" || echo "no package.json"
!test -d .husky && ls -la .husky || echo "no .husky/"

## Your task

1. Confirm prerequisites (git repo + Node project). If `package.json` is missing, ask whether the user still wants Husky.
2. Detect existing Husky/lint-staged setup and summarize what exists.
3. If changes are needed, propose the smallest plan and ask for confirmation (unless `$ARGUMENTS` contains `--yes`).
4. Install/initialize Husky in a repo-compatible way (prefer `npx husky-init`) and ensure a `prepare` script exists.
5. Add/update minimal hooks (confirm before writing):
  - `pre-commit`: run `lint-staged`
  - `pre-push`: run a reasonably fast test/typecheck command if one exists
  - `commit-msg`: add commitlint only if it already exists in the repo
6. Configure `lint-staged` using existing tooling; don’t invent lint/format commands.
7. Explain how to verify hooks and how to temporarily skip them.

## Output

- Detected tooling + current hook state
- Files changed/created
- Commands to verify locally

