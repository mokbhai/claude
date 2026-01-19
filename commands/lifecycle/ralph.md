---
description: Orchestrate autonomous implementation using AI agents (Ralph loop)
argument-hint: '"feature-name" [options]'
---

# Ralph Loop - Autonomous Implementation

purpose: Run autonomous AI agents to implement all stories from breakdown until complete

capabilities:
  - Runs AI agents (Claude Code, OpenCode, Cursor, or Codex) to work through tasks
  - Each agent implements one story, writes tests, and commits changes
  - Repeats until all tasks in breakdown.md are complete
  - Supports multiple AI engines, retry logic, branch-per-task workflow, and PR creation

usage:
  command: ralph-loop.sh <feature-name> [options]
  required:
    - feature-name: Name of the feature (matches plans directory)

ai_engine_options:
  - flag: --claude
    description: Use Claude Code (default)
  - flag: --opencode
    description: Use OpenCode
  - flag: --cursor
    description: Use Cursor agent
  - flag: --codex
    description: Use Codex CLI

workflow_options:
  - flag: --no-tests
    description: Skip writing and running tests
  - flag: --no-lint
    description: Skip linting
  - flag: --fast
    description: Skip both tests and linting

execution_options:
  - flag: --max-iterations N
    description: Stop after N iterations (0 = unlimited)
  - flag: --max-retries N
    description: Max retries per task on failure (default: 3)
  - flag: --retry-delay N
    description: Seconds between retries (default: 5)
  - flag: --dry-run
    description: Show what would be done without executing

git_branch_options:
  - flag: --branch-per-task
    description: Create a new git branch for each task
  - flag: --base-branch NAME
    description: Base branch to create task branches from (default: current)
  - flag: --create-pr
    description: Create a pull request after each task (requires gh CLI)
  - flag: --draft-pr
    description: Create PRs as drafts

other_options:
  - flag: -v, --verbose
    description: Show debug output
  - flag: -h, --help
    description: Show this help
  - flag: --version
    description: Show version number

examples:
  - command: ralph-loop.sh "User Authentication"
    description: Basic usage - run with Claude Code until complete
  - command: ralph-loop.sh "User Authentication" --fast
    description: Fast mode - skip tests and linting
  - command: ralph-loop.sh "User Authentication" --branch-per-task --create-pr
    description: Branch per task workflow with PRs
  - command: ralph-loop.sh "User Authentication" --cursor
    description: Use Cursor agent instead
  - command: ralph-loop.sh "User Authentication" --opencode --max-iterations 20
    description: Limit iterations and use OpenCode
  - command: ralph-loop.sh "User Authentication" --dry-run --verbose
    description: Dry run to see what would happen

architecture:
  ai_engine_support:
    - Claude Code (default)
    - OpenCode
    - Cursor Agent
    - Codex CLI

  directory_structure:
    plans/{feature-name}/:
      - breakdown.md: Stories with [ ] checkboxes
      - design.md: Technical specifications
      - stories/: Story-specific designs
      - implement.md: Implementation guidelines
      - progress.txt: Progress log

  features:
    - Retry logic with configurable attempts
    - Progress monitoring with spinners
    - Token tracking and cost estimation
    - Branch-per-task workflow
    - Automatic PR creation
    - Proper cleanup handlers

execution_loop:
  steps:
    1. Read progress.txt for learnings
    2. Get next task from breakdown.md
    3. Read design.md and story-specific design
    4. Build AI prompt with context
    5. Execute AI agent
    6. Monitor progress with spinner
    7. Parse results and track tokens
    8. Verify task completion
    9. Update breakdown.md (mark [x])
    10. Update progress.txt
    11. Commit changes
    12. Optionally create PR

  termination:
    - condition: All tasks marked [x]
    - condition: max_iterations reached
    - action: Show summary with cost tracking

retry_logic:
  max_retries: 3 (default)
  retry_delay: 5 seconds (default)
  flow:
    - Task starts
    - AI agent execution
    - Success? → YES → Complete task, continue to next
    - Success? → NO → Retry (attempt 2/MAX_RETRIES)
    - All retries failed → Log error, continue to next task

progress_monitoring:
  spinner_states:
    - state: Thinking/Reading code
      color: cyan
    - state: Implementing/Writing tests
      color: magenta
    - state: Testing/Linting
      color: yellow
    - state: Staging/Committing
      color: green

  display_format: "⠙ Implementing │ Create user registration endpoint [02:15]"

token_tracking:
  metrics:
    - Input tokens
    - Output tokens
    - Total tokens
    - Estimated cost (or actual cost for OpenCode)
    - API duration (for Cursor)

  summary_output:
    """
    ============================================
    PRD complete! Finished 15 task(s).
    ============================================

    >>> Cost Summary
    Input tokens:  125000
    Output tokens: 45000
    Total tokens:  170000
    Est. cost:     $1.0875
    ============================================
    """

branch_workflow:
  branch_per_task:
    - Creates branches like: ralph/{task-name-slug}
    - Example: "ralph/create-user-registration-endpoint"
    - Each branch can have its own PR with --create-pr

  options:
    - --base-branch: Specify base branch for task branches
    - --create-pr: Auto-create PR for each task branch
    - --draft-pr: Create PRs as drafts for manual review

breakdown_format:
  structure:
    """
    ## Epic 1: User Registration

    ### Story 1: Create registration endpoint

    - [ ] Implement POST /api/auth/register
    - [ ] Add input validation
    - [ ] Add error handling
    - [ ] Write unit tests
    - [ ] Write integration tests

    ### Story 2: Email verification

    - [ ] Implement verification email
    - [ ] Add verification endpoint
    - [ ] Write tests
    """

  workflow:
    - Ralph finds first [ ] task
    - Implements it completely
    - Changes to [x]
    - Moves to next task
    - Repeats until all are [x]

best_practices:
  setup_phase:
    - Ensure /breakdown and /design are complete
    - Verify all stories have clear checkboxes [ ]
    - Test that AI CLI works independently

  execution_phase:
    - Monitor progress.txt to see learnings
    - Use --dry-run to preview what will happen
    - Keep Ralph running overnight for large features

  completion_phase:
    - Review commits Ralph created
    - Run comprehensive tests
    - Manual code review is recommended

integration:
  lifecycle:
    - /discover → /prd → /breakdown → /design → /ralph-loop.sh → /review → /test → /release
    - Ralph Loop fits after design phase
    - Outputs: Commits, branches, PRs

  position: 5
  steps:
    1: /discover - Find feature requirements
    2: /prd - Create product requirements document
    3: /breakdown - Break down into stories
    4: /design - Create technical design
    5: ralph-loop.sh - Implement autonomously (CURRENT)
    6: /review - Review implementation
    7: /test - Run comprehensive tests
    8: /release - Release the feature

files_used:
  plans/{feature-name}/:
    breakdown.md:
      action: read + update
      description: Tasks to implement
    design.md:
      action: read-only
      description: Technical design
    stories/:
      action: read-only
      description: Story-specific designs
      files:
        - 1.1.md
        - 1.2.md
    implement.md:
      action: read-only
      description: Implementation guidelines
    progress.txt:
      action: create + update
      description: Progress log

troubleshooting:
  issue: Ralph stops early
  solutions:
    - Check if max-iterations is set
    - Check progress.txt for errors
    - Verify AI CLI is installed and working

  issue: Same task failing repeatedly
  solutions:
    - Check progress.txt for error details
    - The design might be incomplete
    - Fix the task manually, mark [x], re-run Ralph

  issue: Token costs too high
  solutions:
    - Use --fast to skip tests during development
    - Use --max-iterations to limit total work
    - Consider using a cheaper AI engine

  issue: Branch workflow issues
  solutions:
    - Ensure clean git state before starting
    - Use --base-branch to specify base explicitly
    - Check that gh CLI is installed for --create-pr

comparison_with_ralphy:
  similarities:
    - Autonomous AI coding loop
    - Multiple AI engine support
    - Retry logic and error handling
    - Progress monitoring
    - Token tracking
    - Branch-per-task workflow

  differences:
    - Integrated with Claude Code lifecycle commands
    - Uses plans/{feature} directory structure
    - Works with breakdown.md format
    - Simpler sequential execution
    - Focused on feature development workflow

future_enhancements:
  - Parallel task execution with git worktrees
  - YAML task format support
  - GitHub Issues integration
  - AI-powered merge conflict resolution
  - Worker dashboard with real-time status
  - Cost optimization strategies
