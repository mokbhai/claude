# Husky Git Hooks Setup Guide

Automated Git hooks setup using Husky for various project types.

## Quick Start

```bash
# Initialize Husky with automatic detection
npx husky-init
```

## Installation by Project Type

### Node.js / JavaScript / TypeScript Projects

```bash
# Install Husky
npm install -D husky

# Initialize Husky
npx husky-init

# Enable Git hooks
npm pkg set scripts.prepare="husky"
```

### Python Projects (with Node for linting tools)

```bash
# Initialize Husky in Python project
npx husky-init
npm install -D husky lint-staged

# Set up pre-commit hook for Python
npx husky set .husky/pre-commit "npx lint-staged"
```

### Frontend Frameworks

#### React / Next.js / Vue / Svelte / Angular

```bash
# Standard installation
npm install -D husky lint-staged
npx husky-init

# Framework-specific pre-commit
npx husky set .husky/pre-commit "npx lint-staged"
```

## Configuration Files

### package.json Setup

```json
{
  "scripts": {
    "prepare": "husky",
    "lint-staged": "lint-staged"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ],
    "*.py": [
      "black",
      "pylint"
    ]
  }
}
```

### Python Projects (.lintstagedrc.json)

```json
{
  "*.{py}": [
    "black",
    "isort",
    "flake8"
  ],
  "*.{md,json,yml,yaml}": [
    "prettier --write"
  ]
}
```

## Common Git Hooks

### Pre-commit Hook (Code Quality)

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx lint-staged
```

### Commit-msg Hook (Conventional Commits)

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx --no -- commitlint --edit $1
```

### Pre-push Hook (Run Tests)

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm test
```

### Post-merge Hook (Install Dependencies)

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm install
```

## Project-Specific Configurations

### Node.js/TypeScript Backend

```json
{
  "lint-staged": {
    "*.ts": ["eslint --fix", "prettier --write"],
    "*.json": ["prettier --write"]
  },
  "devDependencies": {
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0",
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

### React/Next.js Frontend

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{css,scss}": ["stylelint --fix"],
    "*.json": ["prettier --write"]
  },
  "devDependencies": {
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0",
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "stylelint": "^15.0.0"
  }
}
```

### Python Projects

```json
{
  "scripts": {
    "prepare": "husky",
    "lint": "flake8 .",
    "format": "black .",
    "type-check": "mypy ."
  },
  "lint-staged": {
    "*.py": ["black", "isort", "flake8"],
    "*.{md,json,yml}": ["prettier --write"]
  },
  "devDependencies": {
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0",
    "prettier": "^3.0.0"
  }
}
```

**Pyproject.toml:**
```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
```

### Vue.js Projects

```json
{
  "lint-staged": {
    "*.{js,ts,vue}": ["eslint --fix"],
    "*.{css,scss}": ["stylelint --fix"],
    "*.json": ["prettier --write"]
  },
  "devDependencies": {
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0",
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "@vue/eslint-config-prettier": "^9.0.0"
  }
}
```

### Svelte Projects

```json
{
  "lint-staged": {
    "*.{js,ts,svelte}": ["eslint --fix"],
    "*.{css,scss}": ["stylelint --fix"],
    "*.json": ["prettier --write"]
  },
  "devDependencies": {
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0",
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "eslint-plugin-svelte": "^2.0.0"
  }
}
```

### Angular Projects

```json
{
  "lint-staged": {
    "*.{js,ts}": ["eslint --fix"],
    "*.{html,css,scss}": ["prettier --write"],
    "*.json": ["prettier --write"]
  },
  "devDependencies": {
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0",
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0",
    "@angular-eslint/builder": "^17.0.0",
    "@angular-eslint/eslint-plugin": "^17.0.0",
    "prettier": "^3.0.0"
  }
}
```

## Commitlint Configuration

Create `.commitlintrc.json`:

```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [
      2,
      "always",
      ["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci"]
    ],
    "subject-case": [0]
  }
}
```

## Advanced Hooks

### Multi-language Project Hook

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# JavaScript/TypeScript files
echo "Running linters..."
npx lint-staged

# Python files (if any)
if command -v black &> /dev/null; then
  git diff --cached --name-only | grep '\\.py$' | xargs black --check
fi
```

### Branch Name Validation

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

branch=$(git rev-parse --abbrev-ref HEAD)

# Enforce conventional branch names
if ! echo "$branch" | grep -qE '^(feat|fix|docs|style|refactor|test|chore|perf|ci)\/.+$'; then
  echo "Invalid branch name. Use: type/description (e.g., feat/add-login)"
  exit 1
fi
```

### Database Migration Check

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Check for unapplied migrations (Python/Django)
if [ -f "manage.py" ]; then
  python manage.py makemigrations --check --dry-run
fi
```

## Manual Hook Creation

```bash
# Create a custom hook
npx husky set .husky/my-hook "command-to-run"

# Add multiple commands
npx husky add .husky/pre-commit "npm test"
npx husky add .husky/pre-commit "npx lint-staged"
```

## Troubleshooting

### Hooks Not Running

```bash
# Make sure hooks are executable
chmod +x .husky/*

# Reinstall Husky
npm uninstall husky
npm install -D husky
npx husky-init
```

### Debug Hooks

```bash
# Run hook manually
.husky/pre-commit
```

### Skip Hooks (When Needed)

```bash
# Skip pre-commit
git commit --no-verify -m "message"

# Skip commit-msg
git commit --no-verify -m "message"
```

## Best Practices

1. **Keep Hooks Fast**: Use `lint-staged` to only check changed files
2. **Fail Gracefully**: Provide clear error messages
3. **Run Tests Before Push**: Put heavy tests in `pre-push` not `pre-commit`
4. **Enforce Conventional Commits**: Use `commitlint` for consistent messages
5. **Document Hooks**: Add comments explaining complex hooks
6. **Team Consistency**: Commit `.husky` directory to version control
7. **CI/CD Integration**: Don't rely solely on hooks for quality checks

## Complete Example Setup

```bash
# Full setup for a TypeScript project
npm install -D husky lint-staged @commitlint/cli @commitlint/config-conventional eslint prettier
npx husky-init

# Set up hooks
npx husky set .husky/pre-commit "npx lint-staged"
npx husky set .husky/commit-msg "npx --no -- commitlint --edit \$1"

# Configure lint-staged in package.json
npm pkg set lint-staged.'*.{js,jsx,ts,tsx}'[0]="eslint --fix"
npm pkg set lint-staged.'*.{js,jsx,ts,tsx}'[1]="prettier --write"
npm pkg set lint-staged.'*.{json,md}'[0]="prettier --write"
```

## Resources

- [Husky Documentation](https://typicode.github.io/husky)
- [lint-staged](https://github.com/okonet/lint-staged)
- [Commitlint](https://commitlint.js.org)
- [Conventional Commits](https://www.conventionalcommits.org)
