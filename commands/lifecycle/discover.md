---
description: Discovery interview and product vision doc (writes plans/<name>/discovery.md)
argument-hint: "[feature or product name]"
---

# Discover and Define Product Vision

**Document Location**: `plans/$ARGUMENTS/discovery.md`

Conduct initial discovery to understand what to implement and why

## Instructions

Follow this systematic discovery approach for: **$ARGUMENTS**

### Step 0: User Interview

Before starting the discovery process, ask the user:

1. What type of work is this? (new product / new feature / improvement / bug fix)
2. What is driving it? (user feedback / business need / tech debt / market opportunity)
3. What is the primary goal? (solve user problem / revenue / efficiency / learning)
4. What constraints exist? (deadline / resources / required tech stack / legacy integration)

Use the answers to guide the discovery process below.

---

### Step 1: Understand the Context

Based on the interview responses, clarify:
- **Work Type**: [From interview]
- **Motivation**: [From interview]
- **Primary Goal**: [From interview]
- **Constraints**: [From interview]

Additional context to gather:
- Who requested this?
- What is the urgency/priority?
- What happens if we don't do this?

### Step 2: Define the Problem Statement

Ask follow-up questions to understand:
- What specific problem are we solving?
- Who experiences this problem?
- What are the pain points?
- What happens if we don't solve it?
- Are there multiple problems? Which is most important?

### Step 3: Identify Success Metrics

Ask the user:

1. How will you measure success? (adoption / revenue impact / satisfaction / performance)
2. What’s the timeline? (urgent <1w / short 1-4w / medium 1-3m / long 3m+)

### Step 4: Research & Analysis

- Research existing solutions (internal/external)
- Analyze similar features in competitors
- Gather user feedback or data if available
- Identify technical constraints

### Step 5: Define Constraints & Assumptions

Ask the user for the main constraints:

- Existing tech stack that must be used
- Performance targets
- Security/compliance requirements
- Scalability/load expectations

Document:
- Time constraints (deadlines, milestones)
- Resource constraints (team availability, budget)
- Technical constraints (from interview)
- Assumptions we're making (validate these later)

### Step 6: Stakeholder Analysis

Ask the user who the key stakeholders are:

- End users
- Business
- Engineering
- Support / documentation

For each stakeholder:
- Who are they?
- What are their expectations?
- How will this affect them?

### Step 7: Risk Assessment

- What could go wrong?
- What are the dependencies?
- What are the potential blockers?

### Step 8: Create Product Vision

Based on all the information gathered:
- Write a clear, concise vision statement (1-2 sentences)
- Define the target users
- Outline the core value proposition

### Step 9: Document Output

Create a discovery document with the information gathered.

## Output Format

**Document Location**: `plans/$ARGUMENTS/discovery.md`

```markdown
# Discovery: $ARGUMENTS

## Overview
- **Type**: [New Product/Feature/Improvement/Bug Fix]
- **Motivation**: [User Feedback/Business Need/Technical Debt/Market Opportunity]
- **Goal**: [Solve User Problem/Increase Revenue/Improve Efficiency/Learn]
- **Timeline**: [Urgent/Short-term/Medium-term/Long-term]

## Problem Statement
[What problem are we solving?]

## Success Metrics
- [From interview responses]
- Specific targets if available

## Constraints
- Time: [from interview]
- Resources: [from interview]
- Technical: [from interview]
  - Existing tech stack constraints
  - Performance requirements
  - Security/compliance needs
  - Scalability considerations

## Assumptions
- [Assumption 1 to validate]
- [Assumption 2 to validate]

## Stakeholders
[From interview - impact on each group]

## Risks
- [Risk 1]: [mitigation]
- [Risk 2]: [mitigation]

## Product Vision
[1-2 sentence vision statement]

## Interview Summary

### User's Primary Concerns
- [Key concerns expressed during interview]

### Technical Implications Identified
- [Performance considerations]
- [Security considerations]
- [Integration challenges]
- [Scalability needs]

### Tradeoffs Discussed
- [Tradeoff 1]: [chosen approach and rationale]
- [Tradeoff 2]: [chosen approach and rationale]

## Next Steps
- [ ] Proceed to /prd
- [ ] Additional research needed
- [ ] [Other action]
```

## Tips

- Ask "why?" at least 5 times to get to root cause
- Focus on outcomes, not outputs
- Validate assumptions with data when possible
- Keep the vision simple and memorable
- Document everything for future reference
- Use interview responses to tailor the process
- Revisit interview answers if priorities change
