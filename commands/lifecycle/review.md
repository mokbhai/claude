# Code Review Checklist

**Document Location**: `plans/$ARGUMENTS/review.md`

Conduct comprehensive code review for pull request

## Instructions

Follow this systematic code review approach for: **$ARGUMENTS**

1. **Understand the Context**
   - Read the PR description carefully
   - Review the associated story/issue
   - Check the technical design document
   - Understand what problem this solves

2. **Review the Changes**
   - Look at the diff/changes
   - Understand overall approach
   - Identify key files modified

3. **Code Quality Review**
   - Readability and clarity
   - Naming conventions
   - Code organization
   - DRY principle (no duplication)
   - SOLID principles
   - Design patterns used appropriately

4. **Functionality Review**
   - Does it solve the stated problem?
   - All acceptance criteria met?
   - Edge cases handled?
   - Error handling appropriate?

5. **Testing Review**
   - Test coverage adequate?
   - Tests are meaningful?
   - Edge cases tested?
   - Tests are maintainable?

6. **Performance Review**
   - Any obvious performance issues?
   - Database queries optimized?
   - Caching used appropriately?
   - No memory leaks?

7. **Security Review**
   - Input validation present?
   - SQL injection prevented?
   - XSS vulnerabilities avoided?
   - Authentication/authorization correct?
   - Sensitive data protected?

8. **Documentation Review**
   - Code comments where needed?
   - Documentation updated?
   - API docs updated (if applicable)?
   - README updated (if needed)?

9. **Compatibility Review**
   - Backward compatible?
   - Breaking changes documented?
   - Works across browsers/platforms?

10. **Provide Feedback**
    - Be specific and constructive
    - Explain why changes are needed
    - Suggest improvements
    - Acknowledge good work
    - Ask questions if unclear

## Code Review Checklist

### Functionality
- [ ] Solves the stated problem
- [ ] Acceptance criteria met
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] Logic is correct

### Code Quality
- [ ] Code is readable and clear
- [ ] Naming conventions followed
- [ ] Code is well-organized
- [ ] No unnecessary duplication
- [ ] Functions/classes are focused
- [ ] Design patterns used appropriately

### Testing
- [ ] Tests are comprehensive
- [ ] Test coverage is adequate
- [ ] Tests are meaningful
- [ ] Edge cases tested
- [ ] Tests are maintainable

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] Efficient algorithms used
- [ ] No memory leaks
- [ ] Caching used appropriately

### Security
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] XSS vulnerabilities avoided
- [ ] Authentication/authorization correct
- [ ] Sensitive data protected
- [ ] Secrets not hardcoded

### Documentation
- [ ] Code comments where needed
- [ ] Complex logic explained
- [ ] Documentation updated
- [ ] API docs updated (if applicable)
- [ ] README updated (if needed)

### Compatibility
- [ ] Backward compatible
- [ ] Breaking changes documented
- [ ] Cross-browser tested (if frontend)
- [ ] Platform compatibility verified

### Style & Conventions
- [ ] Follows project style guide
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Consistent with rest of codebase

## Review Categories

### Must Fix (Blocking)
Issues that must be addressed before merge:
- Critical bugs
- Security vulnerabilities
- Test failures
- Breaking changes without documentation
- Major logic errors

### Should Fix (Strongly Recommended)
Important improvements:
- Performance issues
- Missing error handling
- Incomplete test coverage
- Confusing code that needs refactoring
- Missing documentation

### Could Fix (Optional)
Nice-to-have improvements:
- Code style inconsistencies
- Minor optimizations
- Extra documentation
- Alternative approaches

### Learning Opportunities
Share knowledge:
- Better patterns or practices
- Alternative implementations
- Relevant resources

## Review Feedback Template

```markdown
## Code Review: [PR Title]

### Overall
[Overall impression - positive, needs work, etc.]

### Must Fix 🚨
1. **[Issue Title]**
   - Location: [file:line]
   - Issue: [description]
   - Suggestion: [how to fix]

### Should Fix ⚠️
1. **[Issue Title]**
   - Location: [file:line]
   - Issue: [description]
   - Suggestion: [how to fix]

### Could Fix 💡
1. **[Suggestion]**
   - Location: [file:line]
   - Why: [reasoning]
   - Suggestion: [improvement]

### Nitpicks 📝
1. **[Minor issue]**
   - Location: [file:line]
   - Suggestion: [style improvement]

### Questions ❓
1. **[Question about approach/implementation]**
   - [question details]

### Kudos 🎉
- [Something done well - be specific]

### Summary
- [ ] Changes requested
- [ ] Approved with changes
- [ ] Approved

## Next Steps
1. Address must-fix items
2. Consider should-fix items
3. Update PR when ready
4. Request re-review if needed
```

## Common Issues to Look For

### Code Smells
```typescript
// ❌ Long function - hard to understand
function processUser(userData) {
  // 50+ lines of logic
}

// ✅ Better - broken down
function processUser(userData) {
  const validated = validateUserData(userData);
  const normalized = normalizeUserData(validated);
  return saveUserData(normalized);
}
```

### Duplicate Code
```typescript
// ❌ Duplicated logic
function calculateDiscountA(price) {
  return price * 0.9;
}

function calculateDiscountB(price) {
  return price * 0.9;
}

// ✅ Better - extracted
function calculateDiscount(price, rate = 0.9) {
  return price * rate;
}
```

### Magic Numbers
```typescript
// ❌ Magic number
setTimeout(() => callback(), 86400000);

// ✅ Better - named constant
const DAY_IN_MS = 24 * 60 * 60 * 1000;
setTimeout(() => callback(), DAY_IN_MS);
```

### Poor Error Handling
```typescript
// ❌ Swallowing errors
try {
  await riskyOperation();
} catch (e) {
  console.error(e);
}

// ✅ Better - proper error handling
try {
  await riskyOperation();
} catch (e) {
  logger.error('Operation failed', e);
  throw new OperationError('Failed to complete operation', e);
}
```

### Missing Tests
```typescript
// ❌ Complex logic without tests
function calculateTax(amount, region) {
  // complex tax calculation logic
  // ... but no tests!
}

// ✅ Better - tested
describe('calculateTax', () => {
  it('calculates correct tax for US region', () => {
    expect(calculateTax(100, 'US')).toBe(10);
  });

  it('handles zero amount', () => {
    expect(calculateTax(0, 'US')).toBe(0);
  });

  it('throws on invalid region', () => {
    expect(() => calculateTax(100, 'INVALID'))
      .toThrow('Invalid region');
  });
});
```

## Tips for Reviewers

### Be Constructive
- Focus on the code, not the person
- Explain the "why" behind suggestions
- Provide examples or alternatives
- Acknowledge good work

### Be Thorough
- Don't rush the review
- Check both code and tests
- Verify acceptance criteria
- Consider security and performance

### Be Timely
- Review promptly
- Respond to questions
- Re-review quickly after updates

### Be Respectful
- Assume good intent
- Ask questions instead of making demands
- Offer to help if needed
- Remember we're all learning

### Be Specific
- Point to exact lines/files
- Explain issues clearly
- Provide actionable feedback
- Link to relevant docs

## Tips for Authors

### Before Requesting Review
- Self-review your changes
- Ensure all tests pass
- Update documentation
- Write a clear PR description
- Address obvious issues first

### During Review
- Be open to feedback
- Ask clarifying questions
- Explain your approach if questioned
- Consider all suggestions seriously
- Learn from the review

### After Review
- Address feedback promptly
- Update PR description if needed
- Request re-review for major changes
- Thank your reviewers

## Review Output Format

```markdown
# Code Review Complete: [PR Title]

## Review Summary
**Overall**: [Approved / Approved with changes / Changes requested]
**Time to review**: [X minutes]
**Files changed**: [X files, Y additions, Z deletions]

## Findings

### Must Fix 🚨
- [ ] [Issue 1]
- [ ] [Issue 2]

### Should Fix ⚠️
- [ ] [Issue 1]
- [ ] [Issue 2]

### Could Fix 💡
- [ ] [Suggestion 1]

### Kudos 🎉
- [What was done well]

## Recommendations
1. [Actionable recommendation 1]
2. [Actionable recommendation 2]

## Final Verdict
- [ ] **Approve** - Ready to merge
- [ ] **Approve with changes** - Minor changes needed
- [ ] **Request changes** - Significant changes needed
- [ ] **Needs discussion** - Questions to resolve

## Next Steps
- [ ] Author to address must-fix items
- [ ] Re-review after updates
- [ ] Merge once approved
```
