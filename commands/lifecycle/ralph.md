# Ralph Loop - Autonomous Implementation

Run Ralph loop to autonomously implement stories from breakdown

## Usage

```bash
/ralph "feature-name" [max-iterations] [sleep-seconds]
```

**Examples**:
```bash
/ralph "User Authentication"        # 10 iterations, 2s sleep (default)
/ralph "User Authentication" 20     # 20 iterations, 2s sleep
/ralph "User Authentication" 50 5   # 50 iterations, 5s sleep
```

## How It Works

The Ralph loop will:

1. **Read** `plans/{feature-name}/breakdown.md` for stories
2. **Find** the first incomplete story
3. **Read** the technical design for that story
4. **Implement** the story with tests
5. **Verify** tests pass
6. **Commit** if successful
7. **Update** progress
8. **Repeat** until all stories complete or max iterations reached

## Document Structure

The breakdown.md should have stories with checkboxes:

```markdown
## Epic 1: User Registration

### Story 1.1: Create registration endpoint
- [ ] Implement POST /api/auth/register
- [ ] Add input validation
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Write integration tests

### Story 1.2: Email verification
- [ ] Implement verification email
- [ ] Add verification endpoint
- [ ] Write tests
```

Ralph will:
- Complete tasks marked `[ ]`
- Mark them complete `[x]` when done
- Commit after each successful story
- Track progress in `progress.txt`

## Progress Tracking

**File**: `plans/{feature-name}/progress.txt`

```markdown
# Ralph Progress for {feature-name}

## Iteration 1 - Story 1.1: Create registration endpoint
- Status: ✅ Complete
- Files changed:
  - src/api/controllers/authController.ts (new)
  - src/services/authService.ts (new)
  - tests/api/auth.test.ts (new)
- Commit: feat: implement registration endpoint with validation
- Learnings:
  - Uses bcrypt for password hashing
  - Validation uses Zod schemas
  - Test database is in-memory SQLite

## Iteration 2 - Story 1.2: Email verification
- Status: ❌ Failed
- Error: Email service not configured
- Next step: Configure email service first
```

## End Conditions

The loop exits when:
- ✅ All stories complete → outputs `<promise>COMPLETE</promise>`
- ❌ Max iterations reached → exits with error
- ⚠️ Critical failure → stops and reports issue

## Safety Features

- **Tests must pass** before marking complete
- **Broken code never committed**
- **Progress tracked** for resume capability
- **Pattern learning** from previous iterations

## Integration with Lifecycle

```
/discover → /prd → /breakdown → /design → /ralph → /review → /test → /release
                                      ↑
                                 Autonomous loop
```

## Files Used

```
plans/{feature-name}/
├── breakdown.md      ← Read for tasks
├── design.md         ← Read for technical details
├── stories/{story}.md← Read for story-specific design
├── implement.md      ← Read for implementation guidelines
└── progress.txt      ← Write/read for learning
```

## Tips

- Start with small max_iterations (10-20) to test
- Use 2-5 second sleep to avoid API rate limits
- Check progress.txt frequently to monitor
- Keep stories small (1-3 hours max)
- Ensure tests are comprehensive before running
- Have rollback plan ready

## Troubleshooting

### Loop not progressing?
- Check progress.txt for errors
- Verify tests are passing
- Check git status for uncommitted changes

### Same iteration repeating?
- Tests might be failing
- Check error messages in progress.txt
- Fix the issue manually and resume

### Too many API calls?
- Increase sleep time (5-10 seconds)
- Reduce max_iterations
- Run overnight with longer delays

## Example Output

```
===========================================
  Iteration 1 of 20
===========================================

Reading breakdown.md...
Found 5 incomplete stories

Working on: Story 1.1 - Create registration endpoint
Reading design: plans/User Auth/stories/1.1-registration.md
Implementing...

Running tests...
✅ 15 tests passing

Committing: feat: implement registration endpoint
Updating breakdown.md...
Appending progress.txt...

Iteration 1 complete. Sleeping 2s...
```
