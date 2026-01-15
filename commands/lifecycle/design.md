# Technical Design for Epic or Story

**Document Location**: `plans/$ARGUMENTS/design.md` (for Epic) or `plans/$ARGUMENTS/stories/{story-name}.md` (for Story)

Create comprehensive technical design document for epic or story implementation

## Instructions

Follow this systematic design approach for: **$ARGUMENTS**

### Step 0: Determine Scope & Interview

First, identify the scope of this design:

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What type of design document do you need?",
        "header": "Design Scope",
        "multiSelect": false,
        "options": [
          {
            "label": "Epic Design",
            "description": "Big picture architecture, multiple stories, high-level design"
          },
          {
            "label": "Story Design",
            "description": "Specific implementation, single story, detailed design"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

Then proceed with the appropriate interview questions below.

---

## Epic Design Interview

### Step 1: Architecture & Integration

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What type of architecture is this?",
        "header": "Architecture",
        "multiSelect": true,
        "options": [
          {
            "label": "Frontend Only",
            "description": "UI/components, no backend changes"
          },
          {
            "label": "Backend Only",
            "description": "API/services, no UI changes"
          },
          {
            "label": "Full Stack",
            "description": "Both frontend and backend changes"
          },
          {
            "label": "Infrastructure",
            "description": "DevOps, databases, cloud services"
          }
        ]
      },
      {
        "question": "Does this integrate with existing systems?",
        "header": "Integration",
        "multiSelect": true,
        "options": [
          {
            "label": "Standalone",
            "description": "No integration needed"
          },
          {
            "label": "Internal APIs",
            "description": "Connects to existing backend services"
          },
          {
            "label": "External APIs",
            "description": "Third-party services or APIs"
          },
          {
            "label": "Database Changes",
            "description": "Schema changes or new tables"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 2: Data & Performance

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What are the performance requirements?",
        "header": "Performance",
        "multiSelect": true,
        "options": [
          {
            "label": "Low Latency",
            "description": "Response time critical (<200ms)"
          },
          {
            "label": "High Throughput",
            "description": "Handle many concurrent requests"
          },
          {
            "label": "Data Intensive",
            "description": "Large datasets, complex queries"
          },
          {
            "label": "Standard Performance",
            "description": "No special performance requirements"
          }
        ]
      },
      {
        "question": "What database considerations apply?",
        "header": "Database",
        "multiSelect": true,
        "options": [
          {
            "label": "New Tables",
            "description": "Creating new data structures"
          },
          {
            "label": "Schema Changes",
            "description": "Modifying existing tables"
          },
          {
            "label": "Data Migration",
            "description": "Migrating existing data"
          },
          {
            "label": "No DB Changes",
            "description": "No database impact"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 3: Security & Compliance

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What security considerations apply?",
        "header": "Security",
        "multiSelect": true,
        "options": [
          {
            "label": "User Data (PII)",
            "description": "Personally identifiable information"
          },
          {
            "label": "Authentication/Authorization",
            "description": "User access control"
          },
          {
            "label": "Data Encryption",
            "description": "Sensitive data protection"
          },
          {
            "label": "API Security",
            "description": "Rate limiting, input validation"
          },
          {
            "label": "Compliance",
            "description": "GDPR, HIPAA, SOC2, etc."
          },
          {
            "label": "No Special Security",
            "description": "Standard security practices"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 4: UI/UX Considerations (if applicable)

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What are the UI/UX considerations?",
        "header": "UI/UX",
        "multiSelect": true,
        "options": [
          {
            "label": "Responsive Design",
            "description": "Mobile, tablet, desktop support"
          },
          {
            "label": "Accessibility",
            "description": "WCAG compliance, screen readers"
          },
          {
            "label": "Real-time Updates",
            "description": "WebSockets, live data"
          },
          {
            "label": "Complex Interactions",
            "description": "Drag-drop, multi-step workflows"
          },
          {
            "label": "No UI Component",
            "description": "Backend or infrastructure only"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 5: Error Handling & Edge Cases

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What error handling strategies are needed?",
        "header": "Error Handling",
        "multiSelect": true,
        "options": [
          {
            "label": "User-Facing Errors",
            "description": "Friendly error messages for users"
          },
          {
            "label": "Retry Logic",
            "description": "Automatic retry for transient failures"
          },
          {
            "label": "Graceful Degradation",
            "description": "Function with reduced capability"
          },
          {
            "label": "Comprehensive Logging",
            "description": "Detailed error tracking"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 6: Testing Strategy

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What testing approach is needed?",
        "header": "Testing",
        "multiSelect": true,
        "options": [
          {
            "label": "Unit Tests",
            "description": "Individual component/function testing"
          },
          {
            "label": "Integration Tests",
            "description": "API and database interaction testing"
          },
          {
            "label": "E2E Tests",
            "description": "Full user journey testing"
          },
          {
            "label": "Performance Tests",
            "description": "Load and stress testing"
          },
          {
            "label": "Security Tests",
            "description": "Vulnerability scanning"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 7: File Structure & Organization

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "How should files be organized?",
        "header": "File Structure",
        "multiSelect": false,
        "options": [
          {
            "label": "Feature-Based",
            "description": "Group by feature/domain"
          },
          {
            "label": "Layer-Based",
            "description": "Group by layer (components, services, utils)"
          },
          {
            "label": "Hybrid",
            "description": "Mix of feature and layer organization"
          },
          {
            "label": "Follow Existing",
            "description": "Match current project structure"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

---

## Story Design Interview

### Step 1: Implementation Approach

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What's the implementation complexity?",
        "header": "Complexity",
        "multiSelect": false,
        "options": [
          {
            "label": "Simple",
            "description": "Straightforward, clear path"
          },
          {
            "label": "Moderate",
            "description": "Some complexity or unknowns"
          },
          {
            "label": "Complex",
            "description": "Multiple components, tricky logic"
          }
        ]
      },
      {
        "question": "What files need to be modified?",
        "header": "File Changes",
        "multiSelect": true,
        "options": [
          {
            "label": "New Files",
            "description": "Creating new components/services"
          },
          {
            "label": "Modify Existing",
            "description": "Updating current files"
          },
          {
            "label": "Delete/Remove",
            "description": "Removing deprecated code"
          },
          {
            "label": "Refactor",
            "description": "Restructuring existing code"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 2: Edge Cases & Validation

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What edge cases need to be handled?",
        "header": "Edge Cases",
        "multiSelect": true,
        "options": [
          {
            "label": "Null/Undefined",
            "description": "Missing data or empty values"
          },
          {
            "label": "Boundary Conditions",
            "description": "Min/max values, limits"
          },
          {
            "label": "Concurrent Access",
            "description": "Race conditions, simultaneous updates"
          },
          {
            "label": "Large Datasets",
            "description": "Performance with lots of data"
          },
          {
            "label": "Invalid Input",
            "description": "Malformed data, wrong types"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

### Step 3: Dependencies & Integration

<AskUserQuestion>
  {
    "questions": [
      {
        "question": "What dependencies exist?",
        "header": "Dependencies",
        "multiSelect": true,
        "options": [
          {
            "label": "Internal Services",
            "description": "Other parts of the codebase"
          },
          {
            "label": "External APIs",
            "description": "Third-party services"
          },
          {
            "label": "Database",
            "description": "Data layer dependencies"
          },
          {
            "label": "No Dependencies",
            "description": "Can be implemented independently"
          }
        ]
      }
    ]
  }
</AskUserQuestion>

---

## Create the Design Document

Based on the interview responses, create a comprehensive design document using the appropriate template below.

## Output Format - Epic Design

**Document Location**: `plans/$ARGUMENTS/design.md`

```markdown
# Technical Design: $ARGUMENTS (Epic)

## 1. Overview
**Epic Goal**: [what this epic achieves]
**Stories Included**: [list of story IDs]
**Dependencies**: [from interview]
**Type**: [Frontend/Backend/Full Stack/Infrastructure]

## 2. Architecture Overview

### Architecture Type
[From interview responses]

### Integration Points
- [ ] Internal APIs: [details]
- [ ] External APIs: [details]
- [ ] Database: [details]

### Component Diagram
```
[Architecture diagram based on interview answers]

Example:
┌─────────────┐         ┌─────────────┐
│  Frontend   │◄───────►│   Backend   │
│  (React)    │  HTTP   │  (Node.js)  │
└─────────────┘         └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │  Database   │
                       │ (PostgreSQL)│
                       └─────────────┘
```

## 3. Data Model

### Database Considerations
[From interview: New tables, schema changes, migrations]

### Schema Changes
[Detailed schema based on interview]

## 4. Performance & Scalability

### Performance Requirements
[From interview]
- Latency targets: [specific requirements]
- Throughput targets: [specific requirements]
- Data volume: [expected scale]

### Optimization Strategy
- [ ] Caching approach
- [ ] Query optimization
- [ ] Indexing strategy
- [ ] Load balancing

## 5. Security & Compliance

### Security Requirements
[From interview]
- [ ] User data protection: [approach]
- [ ] Authentication: [approach]
- [ ] Authorization: [approach]
- [ ] Data encryption: [approach]
- [ ] API security: [approach]
- [ ] Compliance: [requirements]

### Security Implementation
- Input validation: [approach]
- Error handling: [what to expose]
- Logging: [security considerations]

## 6. UI/UX Considerations

### UI Requirements
[From interview if applicable]
- [ ] Responsive design: [approach]
- [ ] Accessibility: [WCAG level, features]
- [ ] Real-time updates: [implementation]
- [ ] Complex interactions: [handling approach]

### Component Structure
[Frontend components to create]

## 7. Error Handling & Edge Cases

### Error Handling Strategy
[From interview]
- User-facing errors: [approach]
- Retry logic: [implementation]
- Graceful degradation: [strategy]
- Logging: [what to log]

### Edge Cases to Handle
[From interview]
- [ ] Null/undefined handling
- [ ] Boundary conditions
- [ ] Concurrent access
- [ ] Large datasets
- [ ] Invalid input

## 8. Testing Strategy

### Testing Approach
[From interview]
- [ ] Unit testing: [framework, coverage target]
- [ ] Integration testing: [scope]
- [ ] E2E testing: [critical paths]
- [ ] Performance testing: [scenarios]
- [ ] Security testing: [approach]

## 9. File Structure & Organization

### Organization Approach
[From interview: Feature-based, Layer-based, Hybrid, Follow existing]

### Directory Structure
```
[Proposed structure]
src/
├── [organization based on interview]
```

## 10. Implementation Order

### Phased Approach
1. **Phase 1**: [first set of stories]
2. **Phase 2**: [second set of stories]
3. **Phase 3**: [remaining stories]

## 11. Technical Decisions & Tradeoffs

### Key Decisions

#### Decision 1: [Title]
- **Context**: [problem or situation]
- **Options Considered**:
  - Option A: [pros/cons]
  - Option B: [pros/cons]
- **Decision**: [chosen approach]
- **Rationale**: [why this choice]
- **Tradeoffs**: [what we're giving up]

[Repeat for major decisions]

## 12. Open Questions
- [Question 1]: [proposed answer or investigation needed]
- [Question 2]: [proposed answer or investigation needed]

## 13. Next Steps
- [ ] Review design with team
- [ ] Get approval for key decisions
- [ ] Proceed to /implement for each story
```

## Output Format - Story Design

**Document Location**: `plans/$ARGUMENTS/stories/{story-name}.md`

```markdown
# Technical Design: $ARGUMENTS (Story)

**Epic**: [Epic name]
**Story**: As a [user], I want [feature], so that [benefit]

## 1. Interview Summary

### Complexity & Scope
- **Complexity**: [Simple/Moderate/Complex]
- **File Changes**: [from interview]
- **Dependencies**: [from interview]

### Key Considerations
- **Edge Cases**: [from interview]
- **Performance**: [from interview]
- **Security**: [from interview]

## 2. Acceptance Criteria Review
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## 3. Component/Module Changes

### Files to Modify
[From interview]
- `src/path/to/file1.ts` - [what changes]
- `src/path/to/file2.ts` - [what changes]

### New Files to Create
[From interview]
- `src/path/to/newFile.ts` - [purpose]

### Function Signatures
```typescript
// New function
function functionName(param1: Type1, param2: Type2): ReturnType {
  // implementation
}
```

## 4. Implementation Steps

1. **Step 1**: [description]
   - [ ] Subtask 1
   - [ ] Subtask 2
   - Verification: [how to verify it works]

2. **Step 2**: [description]
   - Verification: [how to verify it works]

## 5. Edge Cases & Validation

### Edge Cases [From Interview]
| Scenario | Expected Behavior | Implementation |
|----------|-------------------|----------------|
| [Case 1] | [behavior] | [how to implement] |
| [Case 2] | [behavior] | [how to implement] |

### Input Validation
- [Field 1]: [validation rules]
- [Field 2]: [validation rules]

## 6. Error Handling

### Error Scenarios
[From interview]
- [Error 1]: [how to handle]
- [Error 2]: [how to handle]

## 7. Data Changes

### Database Changes (if any)
[From interview]
- **Table**: [table_name]
  - Change: [description]
  - Migration: [file path]

### API Calls (if any)
- **Method**: GET/POST/PUT/DELETE
- **Endpoint**: `/api/path`
- **Request**: [body/params]
- **Response**: [expected response]

## 8. Testing Strategy

### Unit Tests
```typescript
describe('functionName', () => {
  it('should [expected behavior]', () => {
    // test
  });

  it('should handle [edge case from interview]', () => {
    // test
  });
});
```

## 9. Definition of Done
- [ ] Code implemented
- [ ] Edge cases handled [from interview]
- [ ] Unit tests passing (coverage > X%)
- [ ] Integration tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated

## 10. Dependencies [From Interview]
- [ ] [Dependency 1]
- [ ] [Dependency 2]
```

## Tips

**For Epic Design:**
- Use interview responses to tailor architecture
- Document all tradeoffs and alternatives
- Think about testing and observability upfront
- Consider deployment and rollback strategies

**For Story Design:**
- Be specific about implementation steps
- Think about edge cases identified in interview
- Define clear acceptance tests
- Keep stories small enough to complete in 1-3 days

**General:**
- Use diagrams for complex architectures
- Document assumptions from interview
- Get feedback before implementing
- Update design if implementation reveals issues
