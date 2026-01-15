---
description: Run tests and QA for a feature/story and document results
argument-hint: "[feature or story name]"
---

# Run Tests and Quality Assurance

**Document Location**: `plans/$ARGUMENTS/test.md`

Execute comprehensive testing and quality assurance for implemented features

## Instructions

Follow this systematic testing approach for: **$ARGUMENTS**

1. **Understand What to Test**
   - Review the story/feature requirements
   - Review acceptance criteria
   - Review technical design
   - Identify test scope

2. **Unit Testing**
   - Run unit test suite
   - Check test coverage
   - Review test results
   - Fix any failing tests

3. **Integration Testing**
   - Run integration test suite
   - Test API endpoints
   - Test database interactions
   - Test external service integrations

4. **End-to-End Testing**
   - Run E2E test suite
   - Test critical user journeys
   - Test cross-browser compatibility (if frontend)
   - Test on different devices/resolutions (if frontend)

5. **Manual Testing**
   - Test happy path scenarios
   - Test edge cases
   - Test error scenarios
   - Test accessibility (if frontend)
   - Test performance (if applicable)

6. **Regression Testing**
   - Run full test suite
   - Verify no existing features broken
   - Check for side effects
   - Verify data integrity

7. **Performance Testing** (if applicable)
   - Load testing
   - Stress testing
   - Response time verification
   - Memory usage check

8. **Security Testing** (if applicable)
   - Input validation testing
   - Authentication/authorization testing
   - SQL injection testing
   - XSS testing

9. **Accessibility Testing** (if frontend)
   - Keyboard navigation
   - Screen reader compatibility
   - Color contrast
   - Focus indicators

10. **Document Results**
    - Record test results
    - Document any issues found
    - Create bug reports if needed
    - Sign off if all tests pass

## Testing Checklist

### Pre-Testing
- [ ] Code merged to testing branch
- [ ] Database migrations run
- [ ] Environment configured
- [ ] Test data prepared
- [ ] Dependencies installed

### Unit Tests
- [ ] All unit tests passing
- [ ] Test coverage meets threshold
- [ ] No skipped tests (or documented why)
- [ ] Tests run quickly

### Integration Tests
- [ ] All integration tests passing
- [ ] API endpoints tested
- [ ] Database operations tested
- [ ] External services mocked/tested

### End-to-End Tests
- [ ] Critical user journeys tested
- [ ] E2E tests passing
- [ ] Cross-browser tested (if frontend)
- [ ] Different screen sizes tested (if responsive)

### Manual Testing
- [ ] Happy path tested
- [ ] Edge cases tested
- [ ] Error handling tested
- [ ] User flows verified

### Non-Functional Testing
- [ ] Performance acceptable
- [ ] Security verified
- [ ] Accessibility checked (if frontend)
- [ ] Reliability verified

### Regression Testing
- [ ] Existing features still work
- [ ] No data corruption
- [ ] No side effects detected
- [ ] Full test suite passes

## Test Execution Commands

### Running Tests

#### JavaScript/TypeScript (Jest)
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- path/to/test.spec.ts

# Run in watch mode
npm test -- --watch

# Run tests matching pattern
npm test -- --testNamePattern="should login"
```

#### Python (pytest)
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run with verbose output
pytest -v

# Run matching pattern
pytest -k "test_login"
```

#### Ruby (RSpec)
```bash
# Run all tests
rspec

# Run with coverage
rspec --format documentation

# Run specific file
rspec spec/path/to/spec.rb

# Run specific test
rspec spec/path/to/spec.rb:123
```

#### Go
```bash
# Run all tests
go test ./...

# Run with coverage
go test -cover ./...

# Run with verbose output
go test -v ./...

# Run specific test
go test -run TestLogin
```

#### E2E Testing (Playwright/Cypress)
```bash
# Playwright
npx playwright test

# With UI
npx playwright test --ui

# Cypress
npx cypress run

# With UI
npx cypress open
```

## Testing Strategies

### Unit Testing
Focus on individual functions/components in isolation:

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid data', async () => {
      const userData = { email: 'test@example.com', password: 'secure123' };
      const user = await userService.createUser(userData);
      expect(user).toHaveProperty('id');
      expect(user.email).toBe(userData.email);
    });

    it('should throw error for duplicate email', async () => {
      const userData = { email: 'existing@example.com', password: 'secure123' };
      await expect(userService.createUser(userData))
        .rejects
        .toThrow('Email already exists');
    });

    it('should hash password before saving', async () => {
      const userData = { email: 'test@example.com', password: 'plaintext' };
      const user = await userService.createUser(userData);
      expect(user.password).not.toBe('plaintext');
    });
  });
});
```

### Integration Testing
Test how components work together:

```typescript
describe('User Registration API', () => {
  it('should register user via API', async () => {
    const response = await request(app)
      .post('/api/users/register')
      .send({
        email: 'test@example.com',
        password: 'secure123'
      });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('user');
    expect(response.body.user.email).toBe('test@example.com');
  });

  it('should reject duplicate email', async () => {
    await createUser({ email: 'test@example.com', password: 'pass123' });

    const response = await request(app)
      .post('/api/users/register')
      .send({
        email: 'test@example.com',
        password: 'pass123'
      });

    expect(response.status).toBe(409);
  });
});
```

### E2E Testing
Test complete user journeys:

```typescript
test('user can complete registration flow', async ({ page }) => {
  await page.goto('/register');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'secure123');
  await page.click('[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

## Test Coverage Targets

| Type | Minimum Target | Ideal Target |
|------|----------------|--------------|
| Unit Tests | 80% | 90%+ |
| Integration Tests | 70% | 85%+ |
| E2E Tests | Critical paths only | All major flows |
| Overall Coverage | 75% | 85%+ |

## Manual Testing Scenarios

### Happy Path
1. **User Journey**: [step-by-step through feature]
   - Expected: [what should happen]
   - Actual: [what happened]
   - Result: ✅ Pass / ❌ Fail

### Edge Cases
1. **Edge Case**: [description]
   - Input: [test input]
   - Expected: [expected output]
   - Actual: [actual output]
   - Result: ✅ Pass / ❌ Fail

### Error Scenarios
1. **Error**: [type of error]
   - How to trigger: [steps]
   - Expected behavior: [what should happen]
   - Actual behavior: [what happened]
   - Result: ✅ Pass / ❌ Fail

## Accessibility Testing (Frontend)

### Keyboard Navigation
- [ ] Can navigate with Tab key
- [ ] Focus indicators visible
- [ ] Enter/Space activate controls
- [ ] Escape closes modals/menus
- [ ] Skip links work

### Screen Reader
- [ ] Labels announced correctly
- [ ] Form fields have labels
- [ ] Errors announced
- [ ] Semantic HTML used

### Visual
- [ ] Color contrast sufficient (4.5:1 for text)
- [ ] Not color-dependent
- [ ] Text resizable
- [ ] Focus indicators visible

## Performance Testing

### Response Time
- [ ] API responses < 200ms (p95)
- [ ] Page load < 3 seconds
- [ ] Time to Interactive < 5 seconds

### Load Testing
- [ ] Tested with X concurrent users
- [ ] No errors under load
- [ ] Response times acceptable under load

### Memory
- [ ] No memory leaks detected
- [ ] Memory usage within limits
- [ ] Proper cleanup on disposal

## Security Testing

### Input Validation
- [ ] SQL injection tested
- [ ] XSS tested
- [ ] CSRF protection tested
- [ ] Input length limits enforced

### Authentication/Authorization
- [ ] Unauthenticated users rejected
- [ ] Unauthorized users rejected
- [ ] Session management correct
- [ ] Token expiry works

## Test Result Documentation

```markdown
# Test Results: [Feature/Story Name]

## Test Summary
**Date**: [date]
**Tester**: [name]
**Environment**: [dev/staging/production]

## Test Execution

### Unit Tests
- **Framework**: [Jest, pytest, etc.]
- **Total Tests**: [X]
- **Passed**: [Y]
- **Failed**: [Z]
- **Coverage**: [%]

### Integration Tests
- **Total Tests**: [X]
- **Passed**: [Y]
- **Failed**: [Z]

### E2E Tests
- **Total Tests**: [X]
- **Passed**: [Y]
- **Failed**: [Z]

## Manual Testing Results

| Scenario | Expected | Actual | Result |
|----------|----------|--------|--------|
| [Scenario 1] | [expected] | [actual] | ✅/❌ |
| [Scenario 2] | [expected] | [actual] | ✅/❌ |

## Issues Found

### Critical 🚨
1. **[Issue Title]**
   - Description: [what happened]
   - Steps to reproduce: [steps]
   - Expected: [what should happen]
   - Severity: Critical

### High ⚠️
1. **[Issue Title]**
   - Description: [what happened]
   - Steps to reproduce: [steps]

### Medium 💡
1. **[Issue Title]**
   - Description: [what happened]

## Performance Results
- API Response Time: [p50, p95, p99]
- Page Load Time: [time]
- Memory Usage: [usage]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

## Final Verdict
- [ ] **Pass** - Ready for release
- [ ] **Pass with minor issues** - Document, proceed
- [ ] **Fail** - Issues must be fixed

## Sign-off
- [ ] Tests passed
- [ ] Ready for /release
- [ ] Needs re-testing after fixes
```

## Tips

- Write tests before code (TDD)
- Test edge cases, not just happy paths
- Keep tests simple and readable
- Use descriptive test names
- Mock external dependencies
- Test at appropriate boundaries
- Automate repetitive tests
- Review flaky tests
- Keep test data separate
- Use fixtures for complex setup
- Document manual test procedures
- Update tests when requirements change
- Run tests locally before pushing
- Fix broken tests immediately

## Troubleshooting

### Tests Failing
1. Check error messages carefully
2. Verify test environment
3. Check for race conditions
4. Verify mocks/stubs
5. Check test data

### Flaky Tests
1. Identify root cause
2. Add proper waits/expectations
3. Isolate tests properly
4. Fix timing issues
5. Increase test stability

### Low Coverage
1. Identify uncovered code
2. Add tests for uncovered paths
3. Consider if code is needed (dead code?)
4. Refactor for testability
