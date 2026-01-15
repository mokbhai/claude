---
description: Write a technical design doc for an epic or story
argument-hint: "[epic-or-story-name]"
---

# Technical Design for Epic or Story

**Document Location**: `plans/$ARGUMENTS/design.md` (for Epic) or `plans/$ARGUMENTS/stories/{story-name}.md` (for Story)

Create comprehensive technical design document for epic or story implementation

## Instructions

Follow this systematic design approach for: **$ARGUMENTS**

### Step 0: Determine Scope & Interview

First, identify the scope of this design:

Ask the user: is this an **Epic design** (big-picture, multi-story) or a **Story design** (single implementation slice)?

Then proceed with the appropriate interview questions below.

---

## Epic Design Interview

### Step 1: Architecture & Integration

Ask the user:

1. What kind of change is this?
   - frontend-only
   - backend-only
   - full-stack
   - infrastructure (devops/db)
2. What does it integrate with?
   - standalone
   - internal APIs
   - external APIs
   - database changes

### Step 2: Data & Performance

Ask the user:

1. Performance requirements (low latency / high throughput / data-intensive / standard)
2. Database impact (new tables / schema changes / data migration / none)

### Step 3: Security & Compliance

Ask the user what security/compliance considerations apply:

- PII / user data
- authn/authz
- encryption
- API security (validation, rate limiting)
- compliance (GDPR/HIPAA/SOC2/etc)

### Step 4: UI/UX Considerations (if applicable)

If there is UI work, ask the user what matters:

- responsive design targets
- accessibility requirements
- real-time updates
- complex interactions (drag/drop, multi-step)

### Step 5: Error Handling & Edge Cases

Ask the user about error-handling expectations:

- user-facing errors vs silent failures
- retry policy for transient failures
- graceful degradation requirements
- logging/monitoring expectations

### Step 6: Testing Strategy

Ask the user what testing approach is needed:

- unit tests
- integration tests (API/DB)
- end-to-end tests
- performance/load tests
- security tests

### Step 7: File Structure & Organization

Ask the user how this should fit the repo structure:

- follow existing structure (default)
- feature-based grouping
- layer-based grouping
- hybrid

---

## Story Design Interview

### Step 1: Implementation Approach

Ask the user:

1. Implementation complexity (simple / moderate / complex)
2. Expected file changes (new files / modify existing / delete/remove / refactor)

### Step 2: Edge Cases & Validation

Ask the user which edge cases matter:

- missing/null values
- boundary limits
- concurrency/races
- large datasets/performance
- invalid/malformed input

### Step 3: Dependencies & Integration

Ask the user what dependencies exist:

- internal services / other parts of the codebase
- external APIs / third-party services
- database / storage systems
- none (can be implemented independently)

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
