---
description: Overview and usage guide for the lifecycle slash commands
argument-hint: "(no args)"
---

# Software Development Lifecycle Help

Complete guide to the custom software development lifecycle commands

## Overview

This lifecycle provides a structured approach to software development with 8 phases from discovery to release. Each phase has a dedicated command to guide you through the process.

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│ Discovery  │───▶│    PRD     │───▶│  Breakdown │───▶│   Design   │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
     Phase 1          Phase 2          Phase 3          Phase 4

                                                │
                                                ▼
     ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
     │Implement   │◀───│   Ralph    │───▶│   Review   │───▶│    Test    │
     │  (manual)  │    │    Loop    │    │            │    │            │
     └────────────┘    └────────────┘    └────────────┘    └────────────┘
          │               (optional)       Phase 6          Phase 7
          │                                 │
          └─────────────────────────────────┼──────────────┐
                                             ▼              ▼
                                          ┌────────────┐ ┌────────────┐
                                          │  Release   │ │            │
                                          │            │ │            │
                                          └────────────┘ └────────────┘
                                              Phase 8
```

**🆕 Ralph Loop**: Autonomous implementation option - see below

---

## Quick Start

### Starting a New Feature

```bash
# 1. Understand what to build and why
/discover "Your feature or product name"

# 2. Create detailed requirements
/prd "Your feature or product name"

# 3. Break down into independent epics and stories
/breakdown "Your feature or product name"

# 4. Design the technical approach
/design "Epic or Story name"

# 5. Implement the code
/implement "Story name or ID"

# 6. Review the code
/review "PR URL or branch name"

# 7. Test thoroughly
/test "Feature or story name"

# 8. Release to production
/release "Version number (e.g., v1.2.0)"
```

---

## Commands Reference

### Phase 1: `/discover` - Discovery & Vision

**Purpose**: Initial discovery to understand what to implement and why

**When to use**: Starting any new feature, product, or improvement

**What it does**:
- Defines the problem statement
- Identifies success metrics
- Documents constraints and assumptions
- Identifies stakeholders
- Assesses risks
- Creates product vision

**Output**: Discovery document with problem statement, success metrics, constraints, and product vision

**Example**:
```bash
/discover "User Authentication System"
```

---

### Phase 2: `/prd` - Product Requirements Document

**Purpose**: Create comprehensive product requirements document

**When to use**: After discovery phase is complete

**What it does**:
- Defines user personas
- Documents use cases
- Specifies functional requirements
- Specifies non-functional requirements (performance, security, etc.)
- Creates user stories with acceptance criteria
- Defines UI/UX requirements
- Documents data and integration requirements

**Output**: Detailed PRD with all requirements documented

**Example**:
```bash
/prd "User Authentication System"
```

---

### Phase 3: `/breakdown` - Epic & Story Breakdown

**Purpose**: Break down PRD into independent, parallel-executable epics and stories

**When to use**: After PRD is complete and approved

**What it does**:
- Groups related requirements into epics
- Ensures each epic is functionally independent
- Creates stories following INVEST criteria
- Identifies dependencies between stories
- Creates dependency map
- Maximizes parallel execution opportunities

**Key Principles**:
- Each epic should be independently deployable
- Stories should be executable in parallel when possible
- Minimize cross-epic dependencies

**Output**: Epic and story breakdown with dependency matrix

**Example**:
```bash
/breakdown "User Authentication System"
```

---

### Phase 4: `/design` - Technical Design

**Purpose**: Create technical design document for epic or story

**When to use**: Before implementing an epic or story

**What it does**:
- **Epic Design**: Architecture, data model, API design, component structure, key decisions
- **Story Design**: Implementation steps, component changes, edge cases, testing strategy

**Output**: Technical design document with implementation guidance

**Example**:
```bash
/design "Epic 1: User Registration"
/design "Story 1.1: Create registration endpoint"
```

---

### Phase 5: `/implement` - Implementation

**Purpose**: Implement story with comprehensive testing

**When to use**: Ready to write code after design is approved

**What it does**:
- Guides test-first approach (TDD)
- Step-by-step implementation
- Code quality checks
- Self-review process
- Documentation updates
- Pull request creation

**Best Practices**:
- Write tests first (Red-Green-Refactor)
- Run tests frequently
- Commit often with clear messages
- Follow project coding standards

**Output**: Implemented code with tests, ready for review

**Example**:
```bash
/implement "Story 1.1: Create registration endpoint"
```

---

### Phase 6: `/review` - Code Review

**Purpose**: Conduct comprehensive code review

**When to use**: Reviewing a pull request

**What it does**:
- Review code quality and functionality
- Check test coverage
- Assess performance and security
- Verify documentation
- Provide constructive feedback

**Review Categories**:
- **Must Fix**: Blocking issues (security, bugs, tests)
- **Should Fix**: Important improvements (performance, error handling)
- **Could Fix**: Optional improvements (style, optimizations)
- **Learning**: Knowledge sharing opportunities

**Output**: Code review with feedback and approval decision

**Example**:
```bash
/review "PR #123: User registration implementation"
```

---

### Phase 7: `/test` - Testing & QA

**Purpose**: Run comprehensive tests and quality assurance

**When to use**: After implementation, before release

**What it does**:
- Unit testing
- Integration testing
- End-to-end testing
- Manual testing
- Performance testing
- Security testing
- Accessibility testing (if frontend)
- Regression testing

**Output**: Test results with issues documented

**Example**:
```bash
/test "User Authentication Feature"
```

---

### Phase 8: `/release` - Deploy & Release

**Purpose**: Deploy feature to production and manage release process

**When to use**: All testing complete, ready for production

**What it does**:
- Version bumping (following semantic versioning)
- Changelog updates
- Pre-deployment testing
- Deployment execution
- Post-deployment verification
- Rollback plan (if needed)
- Release communication

**Deployment Strategies**:
- Blue-Green Deployment
- Canary Deployment
- Rolling Deployment

**Output**: Released feature with documentation

**Example**:
```bash
/release "v1.2.0"
```

---

## 🆕 Ralph Loop - Parallel Autonomous Implementation

**Purpose**: Spin up multiple parallel workers to autonomously implement all stories

**When to use**: After completing design phase, want fast parallel implementation

**What it does**:
- **Analyzes dependencies** in breakdown.md
- **Creates N worker scripts** that run in parallel
- **Coordinates workers** through shared task queue with locks
- **Runs autonomously** until all stories complete
- **Workers claim available tasks** that have no unmet dependencies

**Usage**:
```bash
/ralph "feature-name" [workers] [max-iterations] [sleep-seconds]
```

**Parameters**:
- `feature-name`: Name from plans directory
- `workers`: Number of parallel workers (default: 3)
- `max-iterations`: Max retry attempts per story (default: 10)
- `sleep-seconds`: Delay between polls (default: 2)

**Examples**:
```bash
# Default: 3 parallel workers
/ralph "User Authentication"

# More workers for large feature with many independent stories
/ralph "User Authentication" 8

# Conservative settings for rate-limited APIs
/ralph "User Authentication" 5 20 5
```

**How It Works**:

**Setup Phase** (runs once):
1. Parses `breakdown.md` for dependencies
2. Creates `task-queue.json` with available/blocked/completed tasks
3. Generates N worker scripts (`workers/worker-{1..N}.sh`)
4. Starts all workers in parallel as background processes

**Worker Loop** (each worker runs continuously):
```
1. Acquire lock on task-queue.json
2. Claim first available task (no unmet dependencies)
3. Release lock
4. Read design, implement, run tests
5. If pass: commit, mark complete, claim next task
6. If fail: record error, release task back to queue
7. Repeat until no tasks available
8. When all workers idle: exit with <promise>COMPLETE</promise>
```

**Architecture**:
```
plans/{feature}/
├── task-queue.json      ← Shared state: available/claimed/completed
├── worker-state.json    ← Worker health tracking
├── progress.txt         ← Combined progress log
└── workers/             ← Generated autonomous scripts
    ├── worker-1.sh
    ├── worker-2.sh
    └── worker-N.sh
```

**Dependency Example**:
```markdown
## Epic 1: User Registration
### Story 1.1: Registration endpoint
- Dependencies: None → Available immediately (Worker 1 claims)

### Story 1.2: Email verification
- Dependencies: Story 1.1 → Blocked until 1.1 completes

## Epic 2: User Profile
### Story 2.1: User model
- Dependencies: None → Available immediately (Worker 2 claims)

### Story 2.2: Profile page
- Dependencies: Story 2.1 → Blocked until 2.1 completes

Result: Workers 1 and 2 run in parallel on 1.1 and 2.1
```

**Progress Tracking**:
```bash
# Real-time monitoring
tail -f plans/{feature}/progress.txt

# Worker status
cat plans/{feature}/worker-state.json | jq '.'

# Task queue
cat plans/{feature}/task-queue.json | jq '.available | length'
```

**Managing Workers**:
```bash
# Stop gracefully (finish current tasks)
pkill -TERM -f "workers/worker-"

# Stop immediately
pkill -KILL -f "workers/worker-"

# Resume after stop
./plans/{feature}/workers/worker-1.sh &
```

**When to Use Ralph Loop**:
- ✅ Multiple independent stories (different epics, components)
- ✅ Clear dependency mapping in breakdown.md
- ✅ Comprehensive technical design completed
- ✅ Tests can verify implementation independently
- ✅ Want to speed up implementation with parallelism

**When NOT to Use Ralph Loop**:
- ❌ All stories have sequential dependencies (no parallelism benefit)
- ❌ No technical design yet
- ❌ Requires human judgment/creativity
- ❌ Critical security/safety implications
- ❌ Tests have shared state/require isolation

**See Also**: `/ralph` command for full documentation

---

## Workflow Examples

### Example 1: New Feature

```bash
# Feature: User Authentication
/discover "User Authentication"
/prd "User Authentication"
/breakdown "User Authentication"

# Epic: User Registration
/design "Epic: User Registration"

# Story: Create registration endpoint
/implement "Story: Create registration endpoint"
/review "PR #45: Registration endpoint"
/test "User Registration"
/release "v1.2.0"
```

### Example 2: Bug Fix

```bash
# For bug fixes, you can skip to later phases
/design "Bug: Login timeout issue"
/implement "Fix: Login timeout"
/review "PR #46: Fix login timeout"
/test "Login timeout fix"
/release "v1.2.1"
```

### Example 3: Refactoring

```bash
# Refactoring existing code
/design "Refactor: Improve user service architecture"
/implement "Refactor: User service"
/review "PR #47: User service refactor"
/test "User service"
/release "v1.3.0"
```

### Example 4: New Feature with Ralph Loop (Parallel Autonomous)

```bash
# Feature: User Authentication with parallel autonomous implementation
/discover "User Authentication"
/prd "User Authentication"
/breakdown "User Authentication"

# Design all epics first (ensure dependencies are marked)
/design "Epic: User Registration"
/design "Epic: User Login"
/design "Epic: Password Reset"

# 🚀 Let Ralph implement all stories with 5 parallel workers
/ralph "User Authentication" 5

# Monitor progress in another terminal
tail -f plans/User\ Authentication/progress.txt

# When complete, review what Ralph built
/review "All PRs from Ralph workers"
/test "User Authentication"
/release "v1.2.0"
```

### Example 5: Mixed Manual + Ralph

```bash
# Feature: E-commerce Checkout
/discover "Checkout System"
/prd "Checkout System"
/breakdown "Checkout System"

# Implement complex parts manually (e.g., payment integration)
/design "Epic: Payment Processing"
/implement "Story: Integrate Stripe"
/review "PR #100: Stripe integration"

# Let Ralph handle simpler stories with 3 parallel workers
/design "Epic: Cart Management"
/ralph "Checkout System" 3

# Monitor workers
cat plans/Checkout\ System/worker-state.json | jq '.'

# Final testing and release
/test "Checkout System"
/release "v2.0.0"
```

---

## Best Practices

### General Workflow
1. **Complete each phase before moving to the next**
2. **Get approvals at key checkpoints** (PRD, design, implementation)
3. **Document everything** for future reference
4. **Communicate with team** at each phase
5. **Learn and improve** after each release

### Phase-Specific Tips

**Discovery**:
- Ask "why?" at least 5 times
- Focus on outcomes, not outputs
- Validate assumptions with data

**PRD**:
- Be specific and measurable
- Prioritize ruthlessly
- Include acceptance criteria

**Breakdown**:
- Minimize dependencies
- Think vertical slices (end-to-end)
- Each epic should be independently valuable

**Design**:
- Document trade-offs
- Consider testing upfront
- Think about deployment and rollback

**Implementation**:
- Follow test-driven development
- Run tests frequently
- Self-review before PR

**Review**:
- Be constructive and specific
- Explain the "why"
- Acknowledge good work

**Testing**:
- Test edge cases, not just happy paths
- Automate what you can
- Document manual procedures

**Release**:
- Have a rollback plan
- Monitor continuously
- Communicate clearly

---

## Common Questions

### Can I skip phases?
For simple changes (bug fixes, small features), you can skip early phases (Discovery, PRD, Breakdown) and start with Design or Implementation.

### How long should each phase take?
It depends on complexity:
- **Small feature**: 1-2 days total
- **Medium feature**: 1-2 weeks total
- **Large feature**: 1-2 months total

### What if I discover issues during implementation?
If you find gaps in the design or requirements:
1. Document the issue
2. Go back to Design or PRD phase
3. Update documentation
4. Get approval if needed
5. Continue implementation

### Can multiple epics be developed in parallel?
Yes! That's the goal of the Breakdown phase. Each epic should be independently developable by different team members.

### How do I handle dependencies between stories?
Document them clearly in the Breakdown phase. If you have many dependencies, consider refactoring your epic boundaries.

---

## Command Aliases

You can also use shortened versions:
- `/disc` - Discovery
- `/plan` - PRD (planning)
- `/break` - Breakdown
- `/arch` - Design (architecture)
- `/impl` - Implementation
- `/cr` - Code Review
- `/qa` - Testing
- `/dep` - Deployment/Release

---

## Getting Help

If you need help with a specific command:
```bash
/help discover    # Help with discovery phase
/help prd         # Help with PRD phase
/help breakdown   # Help with breakdown phase
/help design      # Help with design phase
/help implement   # Help with implementation phase
/help review      # Help with code review
/help test        # Help with testing
/help release     # Help with release
```

Or use the command without arguments to see its full instructions:
```bash
/discover
/prd
/breakdown
/design
/implement
/review
/test
/release
```

---

## Additional Resources

### Related Commands
- `/create-hook` - Create custom hooks
- `/create-command` - Create custom slash commands
- `/refactor` - Refactor code (code/refactor.md)

### Documentation
- Check your project's `CLAUDE.md` for project-specific guidelines
- Review technical design documents before implementing
- Keep documentation updated throughout the lifecycle

---

## Summary

This lifecycle provides a **structured, systematic approach** to software development with:

- ✅ **Clear phases** from idea to production
- ✅ **Independent epics** for parallel development
- ✅ **Comprehensive testing** at each stage
- ✅ **Documentation** throughout the process
- ✅ **Quality checks** before release

**Key Benefits**:
- Reduced rework through upfront planning
- Parallel execution for faster delivery
- Higher quality through comprehensive testing
- Knowledge transfer through documentation
- Predictable, reliable releases

**Next Steps**:
1. Start with `/discover` for your next feature
2. Follow each phase sequentially
3. Adapt the process to your team's needs
4. Continuously improve based on learnings

Happy coding! 🚀
