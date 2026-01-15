# Create Product Requirements Document (PRD)

**Document Location**: `plans/$ARGUMENTS/prd.md`

Generate a comprehensive Product Requirements Document based on discovery phase

## Instructions

Follow this systematic approach to create a PRD for: **$ARGUMENTS**

1. **Review Discovery Document**
   - Ensure discovery phase is complete
   - Review problem statement and success metrics
   - Understand constraints and assumptions
   - Validate product vision

2. **Define User Personas**
   - Who are the primary users?
   - What are their goals and motivations?
   - What are their pain points?
   - What is their skill level?

3. **Document Use Cases**
   - What are the primary use cases?
   - What are the secondary use cases?
   - What are the edge cases?
   - Create user journey flows for each use case

4. **Specify Functional Requirements**
   - What must the product/feature do?
   - List each requirement with a unique ID (FR-001, FR-002, etc.)
   - Prioritize requirements (Must-have, Should-have, Nice-to-have)
   - Define acceptance criteria for each requirement

5. **Specify Non-Functional Requirements**
   - Performance: response times, throughput, latency
   - Security: authentication, authorization, data protection
   - Scalability: concurrent users, data growth
   - Reliability: uptime, error handling, failover
   - Usability: accessibility, learnability
   - Compatibility: browsers, devices, platforms

6. **Define User Stories**
   - Write user stories in format: "As a [user], I want [feature], so that [benefit]"
   - Include acceptance criteria for each story
   - Prioritize using MoSCoW (Must, Should, Could, Won't)

7. **Create User Interface Mockups/Flows**
   - Describe key screens and interactions
   - Create user flow diagrams
   - Define navigation structure
   - Specify responsive behavior

8. **Define Data Requirements**
   - What data needs to be stored?
   - What data needs to be imported/exported?
   - Data retention policies
   - Privacy considerations

9. **Integration Requirements**
   - What systems need to integrate?
   - APIs to use or provide
   - Third-party dependencies
   - Data sync requirements

10. **Documentation & Training**
    - What user documentation is needed?
    - What admin/training materials are needed?
    - Help and support strategy

11. **Create Output Document**
    - Compile all sections into PRD
    - Review with stakeholders
    - Get sign-off before proceeding

## Output Format

```markdown
# Product Requirements Document: [Feature/Product Name]

## 1. Executive Summary
[2-3 paragraph overview of the PRD]

## 2. Problem Statement
[From discovery phase]

## 3. Product Vision
[From discovery phase]

## 4. Success Metrics
[From discovery phase]

## 5. User Personas

### Persona 1: [Name]
- **Role**: [job role]
- **Goals**: [what they want to achieve]
- **Pain Points**: [current problems]
- **Skill Level**: [beginner/intermediate/advanced]

### Persona 2: [Name]
[... repeat for each persona]

## 6. Use Cases

### Use Case 1: [Title]
- **Actor**: [user type]
- **Precondition**: [what must be true before]
- **Main Flow**: [step-by-step interaction]
- **Postcondition**: [result after use case]
- **Alternative Flows**: [error cases, exceptions]

### Use Case 2: [Title]
[... repeat for each use case]

## 7. Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-001 | [description] | Must | [criteria] |
| FR-002 | [description] | Should | [criteria] |
| FR-003 | [description] | Nice | [criteria] |

## 8. Non-Functional Requirements

### Performance
- Response time: [specification]
- Throughput: [specification]
- Latency: [specification]

### Security
- Authentication: [specification]
- Authorization: [specification]
- Data protection: [specification]

### Scalability
- Concurrent users: [specification]
- Data growth: [specification]

### Reliability
- Uptime target: [specification]
- Error handling: [specification]

### Usability
- Accessibility: [WCAG level, etc.]
- Learnability: [specification]

## 9. User Stories

### Epic 1: [Title]
- **Story 1**: As a [user], I want [feature], so that [benefit]
  - Acceptance Criteria:
    - [ ] [Criterion 1]
    - [ ] [Criterion 2]
  - Priority: Must/Should/Could

- **Story 2**: As a [user], I want [feature], so that [benefit]
  - Acceptance Criteria:
    - [ ] [Criterion 1]
    - [ ] [Criterion 2]
  - Priority: Must/Should/Could

## 10. User Interface/Experience

### Key Screens
- **Screen 1**: [description]
- **Screen 2**: [description]

### User Flow
[Diagram or text-based flow description]

## 11. Data Requirements
- Data to store: [list]
- Data sources: [list]
- Retention policy: [specification]
- Privacy considerations: [specification]

## 12. Integration Requirements
- System 1: [integration details]
- System 2: [integration details]
- APIs: [to use or provide]

## 13. Constraints
- Time: [deadlines]
- Resources: [team, budget]
- Technical: [limitations]

## 14. Risks & Mitigation
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [strategy] |

## 15. Open Questions
- [Question 1]: [proposed resolution]
- [Question 2]: [proposed resolution]

## 16. Next Steps
- [ ] Review PRD with stakeholders
- [ ] Get sign-off
- [ ] Proceed to /breakdown
```

## Tips

- Keep requirements specific and measurable
- Focus on "what" not "how"
- Prioritize ruthlessly - not everything can be Must-have
- Include acceptance criteria for each requirement
- Validate with stakeholders before proceeding
- Remember: PRD is a living document, but changes should be deliberate
