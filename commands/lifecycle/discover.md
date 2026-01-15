# Discover and Define Product Vision

**Document Location**: `plans/$ARGUMENTS/discovery.md`

Conduct initial discovery to understand what to implement and why

## Instructions

Follow this systematic discovery approach for: **$ARGUMENTS**

### Step 0: User Interview

Before starting the discovery process, gather key information by interviewing the user:

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What type of work are you planning?",
        "header": "Work Type",
        "multiSelect": false,
        "options": [
          {
            "label": "New Product",
            "description": "Building something from scratch"
          },
          {
            "label": "New Feature",
            "description": "Adding functionality to existing product"
          },
          {
            "label": "Improvement",
            "description": "Enhancing existing functionality"
          },
          {
            "label": "Bug Fix",
            "description": "Fixing issues or defects"
          }
        ]
      },
      {
        "question": "What is driving this work?",
        "header": "Motivation",
        "multiSelect": true,
        "options": [
          {
            "label": "User Feedback",
            "description": "Direct feedback from users"
          },
          {
            "label": "Business Need",
            "description": "Business requirement or goal"
          },
          {
            "label": "Technical Debt",
            "description": "Technical improvements needed"
          },
          {
            "label": "Market Opportunity",
            "description": "Competitive or market-driven"
          }
        ]
      },
      {
        "question": "What is your primary goal?",
        "header": "Goal",
        "multiSelect": false,
        "options": [
          {
            "label": "Solve User Problem",
            "description": "Address pain points for users"
          },
          {
            "label": "Increase Revenue",
            "description": "Drive business growth"
          },
          {
            "label": "Improve Efficiency",
            "description": "Optimize processes or performance"
          },
          {
            "label": "Learn/Explore",
            "description": "Educational or experimental"
          }
        ]
      },
      {
        "question": "What technical constraints exist?",
        "header": "Constraints",
        "multiSelect": true,
        "options": [
          {
            "label": "Tight Deadline",
            "description": "Time-sensitive delivery needed"
          },
          {
            "label": "Limited Resources",
            "description": "Budget or team constraints"
          },
          {
            "label": "Tech Stack Limitations",
            "description": "Must use specific technologies"
          },
          {
            "label": "Legacy Integration",
            "description": "Must work with existing systems"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

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

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "How will you measure success?",
        "header": "Success Metrics",
        "multiSelect": true,
        "options": [
          {
            "label": "User Adoption",
            "description": "Number of users using the feature"
          },
          {
            "label": "Revenue Impact",
            "description": "Direct revenue generation or savings"
          },
          {
            "label": "User Satisfaction",
            "description": "NPS, surveys, feedback"
          },
          {
            "label": "Performance Metrics",
            "description": "Speed, efficiency, reliability"
          }
        ]
      },
      {
        "question": "What is the timeline for this project?",
        "header": "Timeline",
        "multiSelect": false,
        "options": [
          {
            "label": "Urgent (< 1 week)",
            "description": "Critical timeline"
          },
          {
            "label": "Short-term (1-4 weeks)",
            "description": "Quick delivery needed"
          },
          {
            "label": "Medium-term (1-3 months)",
            "description": "Standard project timeline"
          },
          {
            "label": "Long-term (3+ months)",
            "description": "Major initiative"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 4: Research & Analysis

- Research existing solutions (internal/external)
- Analyze similar features in competitors
- Gather user feedback or data if available
- Identify technical constraints

### Step 5: Define Constraints & Assumptions

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What are the main technical constraints?",
        "header": "Tech Constraints",
        "multiSelect": true,
        "options": [
          {
            "label": "Existing Tech Stack",
            "description": "Must work with current technologies"
          },
          {
            "label": "Performance Requirements",
            "description": "Specific performance targets"
          },
          {
            "label": "Security Requirements",
            "description": "Security or compliance needs"
          },
          {
            "label": "Scalability Needs",
            "description": "Must handle significant load"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

Document:
- Time constraints (deadlines, milestones)
- Resource constraints (team availability, budget)
- Technical constraints (from interview)
- Assumptions we're making (validate these later)

### Step 6: Stakeholder Analysis

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "Who are the key stakeholders?",
        "header": "Stakeholders",
        "multiSelect": true,
        "options": [
          {
            "label": "End Users",
            "description": "People who will use the feature"
          },
          {
            "label": "Business Team",
            "description": "Sales, marketing, management"
          },
          {
            "label": "Engineering Team",
            "description": "Developers, DevOps, QA"
          },
          {
            "label": "Support Team",
            "description": "Customer support, documentation"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

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
