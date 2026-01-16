---
description: Diagnose errors and problems in the codebase without solving them
argument-hint: [issue_description]
allowed-tools: Read, Grep, Glob, Bash
---

# Error Diagnosis Mode

You are in **diagnosis mode only**. DO NOT write any code to fix the problem.

## Issue Description

The user is reporting: $ARGUMENTS

## Your Task

Analyze the codebase to understand the issue and provide a comprehensive diagnosis. Follow these steps:

### 1. Understand the Problem
- Identify what the user is trying to do
- Understand the expected vs. actual behavior
- Gather context about the error (if any)

### 2. Locate Related Code
- Search for relevant files using Glob and Grep
- Read the related source files
- Identify the specific functions, methods, or modules involved
- Trace the execution flow to understand the business logic

### 3. Identify the Error
- Pinpoint the exact location of the error (file:line_number)
- Extract the relevant code snippet showing the problematic area
- Explain what the code is currently doing

### 4. Diagnose the Root Cause
- Explain WHY the error is occurring
- Identify the specific logical flaw, bug, or issue
- Show the contrast between what's happening vs. what should happen

### 5. Provide Solution Guidance
- Explain the approach to fix the problem
- Describe the changes needed at a conceptual level
- **DO NOT write any code** - only describe the solution approach

## Output Format

```markdown
# Issue Diagnosis

## Problem Statement
[Brief description of what the user is experiencing]

## Affected Components
- **Files involved**: `file1.py`, `file2.py`
- **Key functions/methods**: `function_name()`, `ClassName.method_name()`

## Root Cause Analysis

### Error Location
**File**: `path/to/file.py:line_number`
**Function**: `function_name()`

### Code Snippet
```python
# Show the problematic code here
```

### What's Happening
[Explain the current behavior]

### What Should Happen
[Explain the expected behavior]

## Diagnosis
[Detailed explanation of the root cause - why is this error occurring?]

## Solution Approach
[Describe how to fix it without writing code - conceptual guidance only]

## Impact Analysis
- What parts of the system are affected?
- Are there any related issues that might occur?
- Priority/severity assessment
```

## Important Constraints

1. **DO NOT write any code** to fix the problem
2. **DO NOT make any file modifications**
3. Focus on understanding and explaining the issue
4. Provide actionable guidance for fixing
5. Reference specific file locations and line numbers
6. Show code snippets only for context/diagnosis purposes
