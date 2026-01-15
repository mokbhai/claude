---
argument-hint: "[description of work]"
description: Create a git worktree with auto-generated branch name from description
allowed-tools:
   - Bash(git worktree:*)
   - Bash(mkdir:*)
   - Bash(grep:*)
   - Bash(cat:*)
   - Bash(test:*)
   - Bash(echo:*)
---

Create a new git worktree at `./worktree/{type}/{description}` for parallel branch development.

## Current worktrees

!git worktree list

## Instructions

1. **Analyze the description** (`$ARGUMENTS`):
   Determine the work type from the description:
   - `feat` - New feature
   - `fix` - Bug fix
   - `refactor` - Code refactoring
   - `perf` - Performance improvement
   - `docs` - Documentation changes
   - `test` - Adding/updating tests
   - `chore` - Maintenance tasks
   - `style` - Code style changes

2. **Generate branch name**:
   - Convert description to kebab-case (lowercase, hyphens instead of spaces)
   - Prefix with type: `{type}/{kebab-case-description}`
   - Keep it concise but descriptive
   - Example: "add user login" → `feat/add-user-login`

3. **Create the worktree**:
   ```bash
   mkdir -p ./worktree
   git worktree add ./worktree/{generated-branch-name} -b {generated-branch-name}
   ```

4. **Add `worktree/` to `.gitignore`**:
   ```bash
   if ! grep -q "^worktree/" .gitignore 2>/dev/null; then
     echo "worktree/" >> .gitignore
     echo "✓ Added 'worktree/' to .gitignore"
   fi
   ```

5. **Verify and report**:
   ```bash
   git worktree list
   ```
   Show the user:
   - ✓ Worktree created at: `./worktree/{generated-branch-name}`
   - 📂 Navigate to it: `cd ./worktree/{generated-branch-name}`
   - 🌳 Branch: `{generated-branch-name}`
   - 🗑️ Remove it: `git worktree remove ./worktree/{generated-branch-name}`

## Examples

- `/worktree add user authentication` → Creates branch `feat/add-user-authentication`
- `/worktree fix memory leak` → Creates branch `fix/memory-leak`
- `/worktree improve api performance` → Creates branch `perf/improve-api-performance`
- `/worktree update readme` → Creates branch `docs/update-readme`
