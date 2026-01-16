---
allowed-tools: *
argument-hint: [epic-file] [epic-id] [options]
description: Execute epic or story tasks from a specified epics file
---

# Execute Epic Task

You are executing epic/story $2 from the file: $1

## Context

- **Epic File**: $1
- **Epic/Story ID**: $2
- **Options**: $ARGUMENTS

## Your Task

1. **Read the Epic/Story**:

- Read the file specified by: $1
- Then find the section for the epic/story with ID "$2"

2. **Understand the Requirements**:
   - Read the Description, Acceptance Criteria, and Technical Tasks
   - Identify any dependencies listed
   - Understand the business value and context

3. **Plan Implementation**: Use the TodoWrite tool to break down all Technical Tasks into actionable items

4. **Execute Implementation**:
   - Write the code as specified in the Technical Tasks
   - Create any new files needed
   - Edit existing files as required
   - Run tests to verify implementation
   - Run `uv run mypy` to ensure type checking passes
   - Follow all acceptance criteria

5. **Update the Epic**: After completing tasks:
   - Mark checkboxes in the Acceptance Criteria section as completed [x]
   - Update any status fields if applicable
   - Add completion notes or comments if needed

6. **Run Code Review**: After implementation and before informing the user:
   - Use the Task tool to launch the `feature-dev:code-reviewer` agent
   - Provide a summary of:
     - The epic/story ID and description
     - What was implemented (changes made, files created/modified)
     - The acceptance criteria that were addressed
   - Let the code-reviewer agent analyze the code for bugs, logic errors, security vulnerabilities, and code quality issues

7. **Inform the User**: After code review is complete, provide a clear summary of:
   - What was implemented
   - Files created/modified (with clickable links)
   - Tests added and results
   - Type checking results (`uv run mypy`)
   - Code review findings (if any issues were found)
   - Any issues encountered
   - What's next (dependencies, remaining tasks)

## Important Notes

- **Write Reusable Code**: Always reuse existing functions, types, and utilities unless:
  - The existing code doesn't provide the required functionality
  - The logic is fundamentally different for the new use case
  - The extra functionality would violate single responsibility principle
- Search the codebase for existing implementations before creating new ones
- Follow the existing code style and patterns in the codebase
- Run `uv run pytest` or appropriate test commands after implementation
- **Run `uv run mypy` to ensure type checking passes** - this is mandatory
- Ensure all imports are correct
- Add proper docstrings following project conventions
- Don't skip dependencies - if a story depends on another, ensure it's complete

## Example Usage

```
/execute-epic plans/api-service-layer-implementation_epics.md EPIC-REPO-001
/execute-epic plans/api-service-layer-implementation_epics.md STORY-REPO-003
/execute-epic REPOSITORY_EPICS.md EPIC-REPO-001
```
