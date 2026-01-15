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

## 🆕 Ralph Loop - Autonomous Implementation

**Purpose**: Automate implementation of stories using Ralph Wiggum technique

**When to use**: After completing design phase, want autonomous implementation

**What it does**:
- Reads breakdown.md for incomplete stories
- Implements one story per iteration
- Runs tests to verify
- Commits if successful
- Learns from previous iterations
- Continues until complete or max iterations

**Usage**:
```bash
# Command form
/ralph "feature-name" [max-iterations] [sleep-seconds]

# Script form (recommended)
./commands/lifecycle/ralph-loop.sh "feature-name" [max-iterations] [sleep-seconds]
```

**Examples**:
```bash
# Default: 10 iterations, 2s sleep
./ralph-loop.sh "User Authentication"

# More iterations for large features
./ralph-loop.sh "User Authentication" 50

# Longer sleep to avoid rate limits
./ralph-loop.sh "User Authentication" 20 5
```

**How It Works**:
```
1. Read plans/{feature}/breakdown.md
2. Find first incomplete story [ ]
3. Read technical design for that story
4. Implement with tests
5. Verify tests pass
6. If pass: commit, mark [x], update progress.txt
7. If fail: record error, try again next iteration
8. Repeat until all [x] or max iterations
```

**Progress Tracking**:
- All progress tracked in `plans/{feature}/progress.txt`
- Learnings carried between iterations
- Failed attempts documented for retry
- Can be stopped and resumed

**When to Use Ralph Loop**:
- ✅ Well-defined stories with clear acceptance criteria
- ✅ Comprehensive technical design completed
- ✅ Tests can verify implementation
- ✅ Repetitive implementation patterns
- ✅ Want to speed up implementation

**When NOT to Use Ralph Loop**:
- ❌ Complex, ambiguous requirements
- ❌ No technical design yet
- ❌ Requires human judgment/creativity
- ❌ Critical security/safety implications
- ❌ First time using this pattern

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

### Example 4: New Feature with Ralph Loop (Autonomous)

```bash
# Feature: User Authentication with autonomous implementation
/discover "User Authentication"
/prd "User Authentication"
/breakdown "User Authentication"

# Design all epics first
/design "Epic: User Registration"
/design "Epic: User Login"
/design "Epic: Password Reset"

# 🚀 Let Ralph implement all stories autonomously
./ralph-loop.sh "User Authentication" 50 3

# Review what Ralph built
/review "PRs from Ralph loop"
/test "User Authentication"
/release "v1.2.0"
```

### Example 5: Mixed Manual + Ralph

```bash
# Feature: E-commerce Checkout
/discover "Checkout System"
/prd "Checkout System"
/breakdown "Checkout System"

# Implement complex parts manually
/design "Epic: Payment Processing"
/implement "Story: Integrate Stripe"
/review "PR #100: Stripe integration"

# Let Ralph handle simpler stories
/design "Epic: Cart Management"
./ralph-loop.sh "Checkout System" 20 2

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
