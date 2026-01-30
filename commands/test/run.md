---
description: Run Playwright tests from markdown test files
argument-hint: <test-filename>
allowed-tools:
  - Bash(*)
  - Read(*)
  - Write(*)
  - Edit(*)
  - mcp__playwright__browser_*
  - mcp__zai-mcp-server__extract_text_from_screenshot
  - mcp__zai-mcp-server__diagnose_error_screenshot
  - AskUserQuestion(*)
---

# Playwright Test Runner

Run automated Playwright tests based on test files in `tests/` directory.

## Usage

```
/test/run <test-filename>
```

**Example**: `/test/run homepage` (runs `tests/homepage.md`)

## Context

!test -f tests/$ARGUMENTS.md && echo "Test file exists" || echo "Test file not found"
!test -f package.json && cat package.json | grep '"scripts"' | head -20 || echo "No scripts found"
!ls tests/*.md 2>/dev/null | head -20 || echo "No test files found"

## Your Task

You are a Playwright test automation agent. Your goal is to:

1. **Parse the test file**: Read `tests/$ARGUMENTS.md` and understand all test flows
2. **Run tests interactively**: Use the Playwright MCP tools to execute each test flow
3. **Generate/Update Playwright script**: Create reusable Playwright TypeScript scripts in `.playwright-mcp/tests/`

## Step-by-Step Instructions

### Step 1: Read and Parse Test File

Read the test file at `tests/$ARGUMENTS.md` and identify:
- Page URL to test
- Pre-conditions and setup requirements
- All test flows with steps and expected results
- Success criteria

### Step 2: Verify Prerequisites

Before running tests:
- Check if dev server is running at expected URL (usually `http://localhost:4321`)
- If not running, ask user to start it with `npm run dev`

### Step 3: Execute Tests Using Playwright MCP

Use these Playwright MCP tools to run the tests:

- `mcp__playwright__browser_navigate` - Navigate to URLs
- `mcp__playwright__browser_snapshot` - Get page accessibility snapshot
- `mcp__playwright__browser_click` - Click elements
- `mcp__playwright__browser_type` - Type text into inputs
- `mcp__playwright__browser_take_screenshot` - Capture screenshots for verification
- `mcp__playwright__browser_console_messages` - Check for console errors
- `mcp__playwright__browser_wait_for` - Wait for conditions

For each test flow:
1. Navigate to starting URL
2. Execute each step in order
3. Verify expected results
4. Report any failures with screenshots

### Step 4: Report Results

After running all test flows, provide a summary:

```
## Test Results: $ARGUMENTS

| Test Flow | Status | Notes |
|-----------|--------|-------|
| Flow 1: [Name] | ✅ PASS / ❌ FAIL | [Details] |
| Flow 2: [Name] | ✅ PASS / ❌ FAIL | [Details] |
| ... | ... | ... |

**Overall**: [X/Y] tests passed

**Console Errors**: [Count] errors found

**Screenshots**: Saved to .playwright-mcp/tests/screenshots/
```

### Step 5: Generate/Update Playwright Script

After all tests pass successfully:

1. **Check if script exists**: Look for `.playwright-mcp/tests/$ARGUMENTS.spec.ts`
2. **If exists**: Update the script with any fixes needed
3. **If not exists**: Create a new Playwright TypeScript test script

The generated script should:
- Use Playwright Test API (`import { test, expect } from '@playwright/test'`)
- Include all test flows from the markdown file
- Have proper assertions for expected results
- Include comments referencing the original markdown test file
- Be runnable with `npx playwright test`

**Script Template**:

```typescript
import { test, expect } from '@playwright/test';

// Generated from tests/$ARGUMENTS.md
// Run with: npx playwright test $ARGUMENTS

test.describe('$ARGUMENTS', () => {
  test.beforeEach(async ({ page }) => {
    // Setup before each test
  });

  test('Flow 1: [Name]', async ({ page }) => {
    await page.goto('http://localhost:4321/');
    // Test steps with assertions
  });

  // Add more test flows...
});
```

## Important Notes

- **Always ask before making significant changes** to existing scripts
- **Take screenshots** of failures for debugging
- **Check console for errors** after each page load
- **Follow mobile-first approach** when testing responsive design
- **Report ALL findings** - both passes and failures

## Available Test Files

To list available test files, the command can be run without arguments to show options.
