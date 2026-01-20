---
description: Create custom subagents with guided configuration including name, description, tools, model, permissions, and hooks
argument-hint: [agent-name] [--user] [--project]
allowed-tools: Read, Write, Bash
---

# Create Custom Subagent

Creating subagent: $1
Scope: ${2:--project}

## Subagent Creation Process

You are creating a custom subagent. Subagents are specialized AI assistants that handle specific types of tasks in their own context window with custom system prompts, specific tool access, and independent permissions.

### Step 1: Determine Scope

Based on the flags provided:
- **--user**: Creates a user-level subagent at `~/.claude/agents/` (available in all projects)
- **--project** (default): Creates a project-level subagent at `.claude/agents/` (available only in this project)

### Step 2: Gather Subagent Configuration

Please provide the following information for the subagent:

1. **Name** (already provided as $1): The unique identifier using lowercase letters and hyphens
   - Example: `code-reviewer`, `data-scientist`, `db-reader`

2. **Description**: When Claude should delegate to this subagent
   - Be specific and clear
   - Include "use proactively" to encourage automatic delegation
   - Example: "Expert code reviewer. Use proactively after code changes to analyze quality, security, and maintainability."

3. **System Prompt**: The instructions that guide the subagent's behavior
   - What should the subagent do when invoked?
   - What are the key workflows or processes?
   - What output format should it use?

4. **Tools**: What tools should the subagent have access to?
   - Leave empty to inherit all tools from parent conversation
   - Specify tools to restrict access: `Read, Grep, Glob, Bash`
   - Examples of tool categories:
     - Read-only: `Read, Grep, Glob`
     - Read-only + terminal: `Read, Grep, Glob, Bash`
     - Full modification: `Read, Write, Edit, Bash, Grep, Glob`

5. **Disallowed Tools** (optional): Any tools to explicitly deny
   - Useful for allowing most tools but blocking specific ones
   - Example: `Write, Edit` (to create a read-only subagent)

6. **Model**: Which AI model should the subagent use?
   - `sonnet`: Balanced capability and speed (default)
   - `opus`: Highest capability for complex tasks
   - `haiku`: Fastest and most economical for simple tasks
   - `inherit`: Use the same model as the main conversation

7. **Permission Mode** (optional): How should the subagent handle permissions?
   - Leave empty for `default` (standard permission checking)
   - `acceptEdits`: Auto-accept file edits
   - `dontAsk`: Auto-deny permission prompts
   - `bypassPermissions`: Skip all permission checks (use with caution!)
   - `plan`: Plan mode (read-only exploration)

8. **Hooks** (optional): Any lifecycle hooks to execute?
   - PreToolUse: Validate operations before execution
   - PostToolUse: Run operations after tool use
   - Stop: Cleanup when subagent finishes

### Step 3: Best Practices

When designing your subagent:

- **Focus on a single task**: Each subagent should excel at one specific domain
- **Write detailed descriptions**: Claude uses the description to decide when to delegate
- **Limit tool access**: Grant only necessary permissions for security and focus
- **Include clear workflows**: Specify step-by-step processes in the system prompt
- **Define output format**: Specify how results should be presented

### Step 4: Common Patterns

Choose a pattern that matches your needs:

**Read-Only Analyzer**: Review code or analyze data without modifications
```yaml
tools: Read, Grep, Glob, Bash
```

**Code Modifier**: Fix bugs, refactor code, implement features
```yaml
tools: Read, Edit, Write, Bash, Grep, Glob
```

**Database Query Executor**: Execute specific commands with validation
```yaml
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
```

### Step 5: Generate Subagent File

Once you provide the configuration, I will create a Markdown file with YAML frontmatter:

**File Location**:
- User-level: `~/.claude/agents/$1.md`
- Project-level: `.claude/agents/$1.md`

**File Format**:
```yaml
---
name: $1
description: [your description]
tools: [selected tools]
model: [selected model]
permissionMode: [optional permission mode]
hooks: [optional hooks]
---

[your system prompt]
```

## Example Subagents

For reference, here are some effective subagent patterns:

### Code Reviewer
Read-only analysis of code quality, security, and best practices
- Tools: Read, Grep, Glob, Bash
- Model: inherit
- Description: "Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code."

### Debugger
Analyze and fix issues with full modification capabilities
- Tools: Read, Edit, Bash, Grep, Glob
- Model: inherit
- Description: "Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues."

### Database Reader
Execute read-only queries with command validation
- Tools: Bash
- Model: sonnet
- Description: "Execute read-only database queries. Use when analyzing data or generating reports."
- Hooks: PreToolUse validation for SELECT-only queries

### Data Scientist
SQL and BigQuery analysis specialist
- Tools: Bash, Read, Write
- Model: sonnet
- Description: "Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries."

## Next Steps

Please provide:
1. A clear description of when Claude should delegate to this subagent
2. The system prompt (instructions for the subagent)
3. Which tools it should have access to (or leave empty to inherit all)
4. Any tools to explicitly deny (optional)
5. Which model to use (sonnet, opus, haiku, or inherit)
6. Permission mode if needed (optional)
7. Any hooks if needed (optional)

I will then create the subagent file at the appropriate location and verify it's ready to use.
