# Break Down into Independent Epics and Stories

**Document Location**: `plans/$ARGUMENTS/breakdown.md`

Break down PRD into independent epics and stories that can be executed in parallel

## Instructions

Follow this systematic breakdown approach for: **$ARGUMENTS**

1. **Review PRD**
   - Ensure PRD is complete and approved
   - Review all functional requirements
   - Review user stories
   - Understand success metrics

2. **Identify Epic Boundaries**
   - Group related requirements/features together
   - Each epic should be:
     - **Functionally independent**: Can be deployed/shipped separately
     - **Parallel-executable**: No blocking dependencies on other epics
     - **Value-delivering**: Provides user value on its own
     - **Testable in isolation**: Can be tested independently
   - Consider natural boundaries: domains, user journeys, architectural layers

3. **Define Epic Criteria**
   - Each epic must have:
     - Clear business value
     - Well-defined scope
     - Independent data model (or shared through clear contracts)
     - Independent API surface (or none)
     - No blocking dependencies on other epics

4. **Break Epics into Stories**
   - Each story should follow **INVEST**:
     - **I**ndependent: Can be done alone
     - **N**egotiable: Details can be discussed
     - **V**aluable: Delivers value
     - **E**stimable: Can be estimated
     - **S**mall: 1-3 days of work
     - **T**estable: Has clear acceptance criteria
   - Each story must include:
     - User story format
     - Acceptance criteria
     - Dependencies (preferably none)
     - Definition of Done

5. **Dependency Analysis**
   - Identify dependencies between stories
   - **Hard dependency**: Story A must finish before Story B starts
   - **Soft dependency**: Story A helps with Story B but not required
   - **Parallel dependency**: Stories can be done simultaneously
   - Goal: Maximize parallel execution

6. **Create Dependency Map**
   - Visualize or document dependencies
   - Identify critical path
   - Identify which stories can be done in parallel
   - Flag any cross-epic dependencies (these should be minimized)

7. **Prioritization**
   - Prioritize epics by business value
   - Prioritize stories within each epic
   - Mark MVP stories (minimum viable product)
   - Identify quick wins

8. **Estimation**
   - Estimate each story in story points or hours
   - Consider complexity, uncertainty, and effort
   - Buffer for unknowns

9. **Review Independence**
   - Final check: Can epics truly be developed in parallel?
   - Are there shared resources that will cause conflicts?
   - Are there unclear boundaries between epics?
   - Refine epic boundaries if needed

10. **Create Output Document**
    - Document all epics and stories
    - Include dependency map
    - Include estimates
    - Create tracking structure (board, milestones, etc.)

## Output Format

```markdown
# Epic & Story Breakdown: [Feature/Product Name]

## Epic Dependencies Overview

```
[Dependency diagram or matrix showing parallel execution paths]
```

**Parallel Execution Strategy**:
- Epic 1 and Epic 2 can be developed simultaneously
- Epic 3 depends on Epic 1 completion
- [etc.]

---

## Epic 1: [Title]

**Business Value**: [why this epic matters]
**Scope**: [what's included]
**Out of Scope**: [what's explicitly excluded]
**Dependencies**: [None / other epics]
**Parallelizable**: Yes/No
**Estimated Effort**: [total story points]

### Stories

#### Story 1.1: [Title]
- **User Story**: As a [user], I want [feature], so that [benefit]
- **Acceptance Criteria**:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
  - [ ] [Criterion 3]
- **Dependencies**: [None / other stories]
- **Can be parallel with**: [Story 1.2, 1.3, etc.]
- **Priority**: Must/Should/Could
- **Estimate**: [story points or hours]
- **Definition of Done**:
  - [ ] Code complete
  - [ ] Unit tests passing
  - [ ] Code reviewed
  - [ ] Documentation updated

#### Story 1.2: [Title]
- **User Story**: As a [user], I want [feature], so that [benefit]
- **Acceptance Criteria**:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
- **Dependencies**: [None / Story 1.1]
- **Can be parallel with**: [Story 1.3, etc.]
- **Priority**: Must/Should/Could
- **Estimate**: [story points or hours]
- **Definition of Done**:
  - [ ] Code complete
  - [ ] Unit tests passing
  - [ ] Code reviewed
  - [ ] Documentation updated

---

## Epic 2: [Title]

**Business Value**: [why this epic matters]
**Scope**: [what's included]
**Out of Scope**: [what's explicitly excluded]
**Dependencies**: [None / other epics]
**Parallelizable**: Yes/No
**Estimated Effort**: [total story points]

### Stories

#### Story 2.1: [Title]
- **User Story**: As a [user], I want [feature], so that [benefit]
- **Acceptance Criteria**:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
- **Dependencies**: [None]
- **Can be parallel with**: [Story 2.2, Epic 1 stories]
- **Priority**: Must/Should/Could
- **Estimate**: [story points or hours]
- **Definition of Done**:
  - [ ] Code complete
  - [ ] Unit tests passing
  - [ ] Code reviewed
  - [ ] Documentation updated

---

## Dependency Matrix

| Story | Depends On | Blocks | Can Parallel With |
|-------|-----------|--------|-------------------|
| Epic 1.1 | None | Epic 1.2 | Epic 2.1, Epic 2.2 |
| Epic 1.2 | Epic 1.1 | None | Epic 2.1, Epic 2.2 |
| Epic 2.1 | None | Epic 2.2 | Epic 1.1, Epic 1.2 |
| Epic 2.2 | Epic 2.1 | None | Epic 1.2 |

---

## Parallel Execution Plan

**Sprint 1** (can all be done simultaneously):
- Epic 1.1 (Team A)
- Epic 2.1 (Team B)

**Sprint 2** (after Sprint 1 complete):
- Epic 1.2 (Team A)
- Epic 2.2 (Team B)

---

## Risk Factors

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | High/Med/Low | [strategy] |
| [Risk 2] | High/Med/Low | [strategy] |

---

## Next Steps

- [ ] Review breakdown with team
- [ ] Assign stories to team members
- [ ] Proceed to /design for each epic
- [ ] Create tracking board (Jira, GitHub Projects, etc.)
```

## Independence Checklist

For each Epic, verify:

- [ ] Can be deployed independently?
- [ ] Has its own test suite?
- [ ] No blocking dependencies on other epics?
- [ ] Clear API contracts with other epics (if any)?
- [ ] Separate database schema or clear ownership?
- [ ] Can be worked on by separate team member?
- [ ] Has its own branch strategy?

For each Story, verify:

- [ ] INVEST criteria met?
- [ ] Acceptance criteria are testable?
- [ ] Definition of Done is clear?
- [ ] No hard dependencies (or clearly documented)?
- [ ] Can be completed in 1-3 days?

## Tips

- Start with user journey, not technical architecture
- Minimize cross-epic dependencies
- When in doubt, make epics smaller and more focused
- Each epic should be releasable on its own
- Document dependencies clearly
- Use visual diagrams for complex dependencies
- Revisit breakdown if you discover many dependencies
- Consider "vertical slices" (end-to-end features) over "horizontal slices" (layers)
