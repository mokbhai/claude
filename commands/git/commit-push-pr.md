---
description: Commit changes, push branch, and open a GitHub pull request
argument-hint: "[--no-verify] [extra context]"
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git push:*)
  - Bash(git restore:*)
  - Bash(git reset:*)
  - Bash(git branch:*)
  - Bash(git rev-parse:*)
  - Bash(git log:*)
  - Bash(gh:*)
  - Bash(ls:*)
  - Bash(test:*)
  - Bash(cat:*)
  - Bash(head:*)
---

# Commit, Push & PR

This command creates well-formatted commits, pushes them to the remote repository, and creates a pull request - all in one seamless workflow.

## Usage

To commit, push, and create a PR, just type:

```
/commit-push-pr
```

Or with options:

```
/commit-push-pr --no-verify
```

## What This Command Does

## Context

!git branch --show-current || true
!git status --porcelain=v1 || true
!git diff --staged || true
!git log --oneline -10 || true
!test -f package.json && cat package.json | head -n 120 || true
!gh --version || true

1. **Pre-commit Checks** (unless `--no-verify` is present in `$ARGUMENTS`):
   - Run repo-appropriate checks (lint/build/tests) if they exist.
   - Don’t assume a package manager; detect from the repo.

2. **Branch Management**:
   - If on `main` or `master`, creates a new feature branch
   - Uses branch name based on the commit type (e.g., `feat/feature-name`, `fix/bug-name`)

3. **Commit Creation**:
   - Checks which files are staged with `git status`
   - If 0 files are staged, automatically adds all modified and new files with `git add`
   - Performs a `git diff` to understand what changes are being committed
   - Analyzes the diff to determine if multiple distinct logical changes are present
   - If multiple distinct changes are detected, suggests breaking the commit into multiple smaller commits
   - Creates commit message(s) using emoji conventional commit format

4. **Push to Remote**:
   - Pushes the branch to `origin` with `-u` flag to set upstream tracking

5. **Pull Request Creation**:
   - Creates a PR using `gh pr create`
   - Auto-generates PR title from the commit message(s)
   - Auto-generates PR description from all commits in the branch
   - Groups commits by type for better organization
   - Includes a summary of changes, test plan, and checklist

## Best Practices

### Commits

- **Atomic commits**: Each commit should contain related changes that serve a single purpose
- **Conventional commit format**: Use the format `<type>: <description>`
- **Present tense, imperative mood**: Write commit messages as commands
- **Concise first line**: Keep the first line under 72 characters

### Branches

- **Descriptive names**: Use branch names like `feat/user-auth`, `fix/memory-leak`, `refactor/api-calls`
- **Scope prefixes**: Use type prefixes to indicate the purpose (feat/, fix/, chore/, etc.)
- **Kebab-case**: Use hyphens to separate words in branch names

### Pull Requests

- **Clear titles**: PR title should summarize the change (generated from first commit)
- **Structured description**: Organized with sections for Summary, Changes, Testing, Checklist
- **Linked issues**: Include issue references like `Closes #123` or `Relates to #456`

## Commit Types and Emojis

- ✨ `feat`: New feature
- 🐛 `fix`: Bug fix
- 📝 `docs`: Documentation
- 💄 `style`: Formatting/style
- ♻️ `refactor`: Code refactoring
- ⚡️ `perf`: Performance improvements
- ✅ `test`: Tests
- 🔧 `chore`: Tooling, configuration
- 🚀 `ci`: CI/CD improvements
- 🗑️ `revert`: Reverting changes
- 🧪 `test`: Add a failing test
- 🚨 `fix`: Fix compiler/linter warnings
- 🔒️ `fix`: Fix security issues
- 👥 `chore`: Add or update contributors
- 🚚 `refactor`: Move or rename resources
- 🏗️ `refactor`: Make architectural changes
- 🔀 `chore`: Merge branches
- 📦️ `chore`: Add or update compiled files or packages
- ➕ `chore`: Add a dependency
- ➖ `chore`: Remove a dependency
- 🌱 `chore`: Add or update seed files
- 🧑‍💻 `chore`: Improve developer experience
- 🧵 `feat`: Add or update code related to multithreading or concurrency
- 🔍️ `feat`: Improve SEO
- 🏷️ `feat`: Add or update types
- 💬 `feat`: Add or update text and literals
- 🌐 `feat`: Internationalization and localization
- 👔 `feat`: Add or update business logic
- 📱 `feat`: Work on responsive design
- 🚸 `feat`: Improve user experience / usability
- 🩹 `fix`: Simple fix for a non-critical issue
- 🥅 `fix`: Catch errors
- 👽️ `fix`: Update code due to external API changes
- 🔥 `fix`: Remove code or files
- 🎨 `style`: Improve structure/format of the code
- 🚑️ `fix`: Critical hotfix
- 🎉 `chore`: Begin a project
- 🔖 `chore`: Release/Version tags
- 🚧 `wip`: Work in progress
- 💚 `fix`: Fix CI build
- 📌 `chore`: Pin dependencies to specific versions
- 👷 `ci`: Add or update CI build system
- 📈 `feat`: Add or update analytics or tracking code
- ✏️ `fix`: Fix typos
- ⏪️ `revert`: Revert changes
- 📄 `chore`: Add or update license
- 💥 `feat`: Introduce breaking changes
- 🍱 `assets`: Add or update assets
- ♿️ `feat`: Improve accessibility
- 💡 `docs`: Add or update comments in source code
- 🗃️ `db`: Perform database related changes
- 🔊 `feat`: Add or update logs
- 🔇 `fix`: Remove logs
- 🤡 `test`: Mock things
- 🥚 `feat`: Add or update an easter egg
- 🙈 `chore`: Add or update .gitignore file
- 📸 `test`: Add or update snapshots
- ⚗️ `experiment`: Perform experiments
- 🚩 `feat`: Add, update, or remove feature flags
- 💫 `ui`: Add or update animations and transitions
- ⚰️ `refactor`: Remove dead code
- 🦺 `feat`: Add or update code related to validation
- ✈️ `feat`: Improve offline support

## PR Description Template

The auto-generated PR description follows this structure:

```markdown
## Summary

[Brief 1-3 bullet points describing what this PR does]

## Changes

[Detailed list of changes, grouped by commit type]

- ✨ **Features**: ...
- 🐛 **Bug Fixes**: ...
- 📝 **Documentation**: ...
- 🔧 **Chores**: ...

## Test Plan

[Bulleted checklist of testing completed]

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases covered

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
```

## Guidelines for Splitting Commits

When analyzing the diff, consider splitting commits based on:

1. **Different concerns**: Changes to unrelated parts of the codebase
2. **Different types of changes**: Mixing features, fixes, refactoring, etc.
3. **File patterns**: Changes to different types of files (e.g., source code vs documentation)
4. **Logical grouping**: Changes that would be easier to understand or review separately
5. **Size**: Very large changes that would be clearer if broken down

## Examples

**Single feature commit:**

```
Branch: feat/user-authentication
Commit: ✨ feat: add JWT-based user authentication
PR Title: ✨ feat: add JWT-based user authentication
```

**Multi-commit PR:**

```
Branch: fix/payment-processing

Commits:
- 🐛 fix: resolve race condition in payment processing
- ✅ test: add unit tests for payment race condition
- 📝 docs: document payment processing edge cases

PR Title: 🐛 fix: resolve race condition in payment processing
PR Description includes all commits grouped by type
```

**Complex feature with multiple parts:**

```
Branch: feat/api-redesign

Commits:
- ✨ feat: add new REST API endpoints
- ♻️ refactor: simplify data access layer
- 📝 docs: update API documentation
- 🔧 chore: update dependencies for new API
- ✅ test: add integration tests for new endpoints
- 🚨 fix: resolve linting issues in new code

PR Title: ✨ feat: add new REST API endpoints
PR Description organizes all commits by type
```

## Command Options

- `--no-verify`: Skip running the pre-commit checks (lint, build, generate:docs)

## Important Notes

- **Pre-commit checks** run by default to ensure code quality
- If checks fail, you'll be asked if you want to proceed anyway or fix the issues
- **Branch creation** happens automatically if on main/master
- **Upstream tracking** is set automatically with `-u` flag
- **PR title** comes from the first (or primary) commit message
- **PR description** is auto-generated from all commits in the branch
- If suggesting multiple commits, the workflow will help stage and commit separately before pushing
- The command reviews all diffs to ensure commit messages match the changes
- **GitHub CLI (`gh`)** must be installed and authenticated for PR creation

## Troubleshooting

**If `gh` is not installed:**

```bash
brew install gh
gh auth login
```

**If branch already exists on remote:**

- The command will still push new commits
- Existing PR will be updated with new commits

**If pre-commit checks fail:**

- Review the error output
- Fix issues and run `/commit-push-pr` again
- Or use `--no-verify` to skip checks (not recommended)
