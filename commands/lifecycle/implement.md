---
description: Implement a story from the design, with tests and a PR-ready checklist
argument-hint: "[story name or ID]"
---

# Implement Story with Tests

**Document Location**: `plans/$ARGUMENTS/implement.md`

Implement a story following the technical design with comprehensive testing

## Instructions

Follow this systematic implementation approach for: **$ARGUMENTS**

### Step 0: Implementation Interview

Before starting implementation, gather key details:

Ask the user:

1. What testing approach should be used? (TDD / alongside / after / minimal)
2. What type of code is being implemented? (Frontend/UI / Backend/API / Database / Infrastructure)
3. Are there specific performance requirements? (critical / standard / not performance critical)
4. What level of error handling is needed? (comprehensive / standard / basic)

Use the answers to guide the implementation approach below.

---

## Implementation Steps

### 1. Pre-Implementation Setup
   - Review the technical design document
   - Review acceptance criteria
   - Ensure design is approved
   - Check that all dependencies are complete
   - Create or switch to feature branch: `git checkout -b feature/story-id-description`

2. **Understand the Context**
   - Read existing related code
   - Understand the codebase patterns and conventions
   - Review CLAUDE.md for project-specific guidelines
   - Check existing tests for similar functionality

3. **Test-First Approach (TDD)**
   - Write tests BEFORE implementation
   - Start with failing tests (Red)
   - Implement to make tests pass (Green)
   - Refactor if needed (Refactor)

4. **Implementation Steps**
   - Follow the technical design implementation steps
   - Implement incrementally
   - Run tests frequently
   - Commit often with descriptive messages

5. **Code Quality**
   - Follow project coding standards
   - Write clean, readable code
   - Add appropriate comments (only when needed)
   - Ensure proper error handling
   - Handle edge cases

6. **Self-Review**
   - Review your own code before creating PR
   - Check against acceptance criteria
   - Ensure tests are comprehensive
   - Run full test suite
   - Check for console errors/warnings
   - Verify accessibility (if frontend)

7. **Documentation**
   - Update relevant documentation
   - Add/update code comments where needed
   - Update README or API docs (if applicable)

8. **Create Pull Request**
   - Draft PR with clear description
   - Reference the story/design documents
   - Include screenshots (if frontend)
   - Link to related issues/tickets

9. **Address Feedback**
   - Monitor PR for review comments
   - Address feedback promptly
   - Add requested tests
   - Update documentation as requested

10. **Final Checks**
    - All tests passing
    - Code reviewed and approved
    - Documentation updated
    - Ready for merge

## Implementation Checklist

### Before Starting
- [ ] Technical design reviewed and approved
- [ ] Acceptance criteria understood
- [ ] Dependencies completed
- [ ] Branch created from latest main
- [ ] Development environment ready

### During Implementation
- [ ] Tests written first (TDD)
- [ ] Implementation follows design
- [ ] Code follows project conventions
- [ ] Error handling implemented
- [ ] Edge cases covered
- [ ] Code is clean and readable
- [ ] Tests are comprehensive

### Before PR
- [ ] All tests passing (unit + integration)
- [ ] Linting passes
- [ ] Type checking passes (if applicable)
- [ ] No console errors/warnings
- [ ] Self-review completed
- [ ] Code committed with clear messages

### PR Creation
- [ ] PR description clear and complete
- [ ] References story/design documents
- [ ] Screenshots included (if applicable)
- [ ] Tests demonstrate functionality
- [ ] Documentation updated

### After Review
- [ ] Reviewer feedback addressed
- [ ] All requested changes made
- [ ] Tests added/updated
- [ ] Approved for merge

## Best Practices

### Code Quality
```typescript
// ✅ Good: Clear, descriptive names
function calculateUserAge(birthDate: Date): number {
  const today = new Date();
  const ageInMs = today.getTime() - birthDate.getTime();
  return Math.floor(ageInMs / (1000 * 60 * 60 * 24 * 365));
}

// ❌ Bad: Unclear, generic names
function calc(d: Date): number {
  const n = new Date();
  const x = n.getTime() - d.getTime();
  return Math.floor(x / 31536000000);
}
```

### Error Handling
```typescript
// ✅ Good: Specific error handling
async function fetchUser(id: string) {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (error instanceof NotFoundError) {
      throw new UserNotFoundError(id);
    }
    throw new ApiError('Failed to fetch user', error);
  }
}

// ❌ Bad: Generic error swallowing
async function fetchUser(id: string) {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}
```

### Testing
```typescript
// ✅ Good: Descriptive test with clear assertions
describe('calculateUserAge', () => {
  it('should return correct age for a given birth date', () => {
    const birthDate = new Date('1990-01-01');
    const age = calculateUserAge(birthDate);
    expect(age).toBeGreaterThanOrEqual(34);
  });

  it('should handle future dates', () => {
    const futureDate = new Date('2050-01-01');
    expect(() => calculateUserAge(futureDate)).toThrow();
  });
});

// ❌ Bad: Vague test, poor assertions
describe('calculateUserAge', () => {
  it('works', () => {
    const result = calculateUserAge(new Date('1990-01-01'));
    expect(result).toBeTruthy();
  });
});
```

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
feat: add user authentication login

- Implement login endpoint with JWT tokens
- Add password hashing with bcrypt
- Add input validation for email and password
- Write unit tests for login service

Closes #123
```

```
test: add integration tests for user registration

- Test successful registration
- Test duplicate email error
- Test validation errors

Related to #124
```

## PR Description Template

```markdown
## Summary
Brief description of what this PR implements

## Story
- Story ID: #[number]
- Title: [Story title]
- Design doc: [link to technical design]

## Changes
- [ ] New feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Tests
- [ ] Documentation

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows project standards
- [ ] All tests passing
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts

## Notes
[Any additional context for reviewers]
```

## Troubleshooting

### Tests Failing
1. Check test error messages carefully
2. Verify test data is correct
3. Check for race conditions
4. Verify mocks/stubs are configured correctly

### Linting Errors
1. Read error messages carefully
2. Run linter with auto-fix if available
3. Check project style guide
4. Ask for help if needed

### Merge Conflicts
1. Pull latest changes from main
2. Resolve conflicts locally
3. Test thoroughly after resolving
4. Communicate with conflicting author if needed

## Tips

- Write tests first - it leads to better design
- Run tests frequently - catch issues early
- Commit often - smaller commits are easier to review
- Ask questions if design is unclear
- Communicate blockers early
- Take pride in your code quality
- Think about maintainability
- Consider performance implications
- Handle errors gracefully
- Document non-obvious logic

## Output Format

After implementation, provide:

```markdown
# Implementation Complete: [Story ID - Story Title]

## Summary
[What was implemented]

## Changes Made
- **Files Modified**: [list files]
- **Files Created**: [list files]
- **Tests Added**: [test files and coverage]

## Testing
- [ ] Unit tests: X passing, Y failing
- [ ] Integration tests: X passing, Y failing
- [ ] Manual testing: [results]

## PR
- **Branch**: `feature/story-id-description`
- **PR Link**: [link once created]

## Definition of Done
- [ ] Code complete
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Ready for merge

## Notes
[Any additional notes or blockers]
```
