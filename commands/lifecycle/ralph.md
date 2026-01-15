# Ralph Loop - Parallel Autonomous Implementation

**Purpose**: Set up and manage parallel autonomous agents to implement all stories from breakdown

**What it does**:
- Creates worker scripts that run in parallel when stories are independent
- Analyzes dependencies to schedule work efficiently
- Coordinates workers through shared state management
- Runs autonomously until all stories are complete

## Usage

```bash
/ralph "feature-name" [workers] [max-iterations-per-story] [sleep-seconds]
```

**Parameters**:
- `feature-name`: Name of the feature (matches plans directory)
- `workers`: Number of parallel workers (default: 3)
- `max-iterations-per-story`: Max retry attempts per story (default: 10)
- `sleep-seconds`: Delay between worker polls (default: 2)

**Examples**:
```bash
/ralph "User Authentication"              # 3 workers, 10 iterations each, 2s sleep
/ralph "User Authentication" 5            # 5 parallel workers
/ralph "User Authentication" 8 20 3       # 8 workers, 20 iterations, 3s sleep
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Ralph Orchestration Layer                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  plans/{feature-name}/                                           │
│  ├── breakdown.md         → Stories with dependencies           │
│  ├── design.md            → Technical specifications             │
│  ├── stories/             → Story-specific designs               │
│  ├── implement.md         → Implementation guidelines            │
│  ├── task-queue.json      → Available tasks (lock-protected)     │
│  ├── worker-state.json    → Worker status coordination           │
│  ├── progress.txt         → Combined progress log               │
│  └── workers/             → Generated worker scripts             │
│      ├── worker-1.sh                                         │
│      ├── worker-2.sh                                         │
│      └── worker-N.sh                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## How It Works

### Phase 1: Setup (One-Time)

When you run `/ralph "feature-name"`, the system:

1. **Analyzes Dependencies** from `breakdown.md`
   ```markdown
   ## Epic 1: User Registration
   ### Story 1.1: Create registration endpoint
   - Depends on: None
   - [ ] Implement endpoint
   ### Story 1.2: Email verification
   - Depends on: Story 1.1
   - [ ] Implement verification
   ```

2. **Creates Task Queue** (`task-queue.json`)
   ```json
   {
     "available": ["1.1", "2.1", "3.1"],
     "in-progress": {},
     "completed": [],
     "dependencies": {
       "1.2": ["1.1"],
       "2.2": ["2.1"]
     }
   }
   ```

3. **Generates N Worker Scripts** (`workers/worker-{1..N}.sh`)
   - Each worker is an independent script
   - Workers poll the shared task queue
   - Workers claim tasks using atomic file locking
   - Workers run until all tasks complete

4. **Starts All Workers in Parallel**
   ```bash
   # Background processes that run autonomously
   ./workers/worker-1.sh &
   ./workers/worker-2.sh &
   ./workers/worker-3.sh &
   ```

### Phase 2: Worker Execution Loop

Each worker continuously:

1. **Acquire Lock** on `task-queue.json`
2. **Check** if any tasks are:
   - Available (no unmet dependencies)
   - Not already claimed by another worker
3. **Claim Task** by moving it to "in-progress"
4. **Release Lock**
5. **Read Design** for the claimed story
6. **Implement** with tests
7. **Run Tests** (type check, lint, test suite)
8. **Update State**:
   - **If pass**: Mark complete, commit, claim next task
   - **If fail**: Release task back to queue, record error
9. **Repeat** until no tasks available

### Phase 3: Dependency Resolution

```
Initial State:
  Task 1.1 [No deps]     → Worker 1 claims ✓
  Task 1.2 [Depends: 1.1] → Blocked until 1.1 completes
  Task 2.1 [No deps]     → Worker 2 claims ✓
  Task 2.2 [Depends: 2.1] → Blocked until 2.1 completes
  Task 3.1 [No deps]     → Worker 3 claims ✓

After Worker 1 completes 1.1:
  Task 1.2 becomes available → Worker 1 (or any worker) claims
```

## Coordination Mechanism

### Shared State Files

**`task-queue.json`** - Thread-safe task distribution
```json
{
  "available": ["2.1", "3.1"],
  "in-progress": {"1.1": "worker-1"},
  "completed": [],
  "failed": {},
  "dependencies": {"1.2": ["1.1"]},
  "last-updated": "2025-01-15T10:30:00Z"
}
```

**`worker-state.json`** - Worker health tracking
```json
{
  "worker-1": {
    "status": "working",
    "current-task": "1.1",
    "tasks-completed": 3,
    "last-heartbeat": "2025-01-15T10:30:05Z"
  },
  "worker-2": {
    "status": "idle",
    "current-task": null,
    "tasks-completed": 2,
    "last-heartbeat": "2025-01-15T10:30:04Z"
  }
}
```

### Lock Protocol

```bash
# Worker claiming a task
acquire_lock() {
  local lockfile="plans/${FEATURE}/.taskqueue.lock"
  local timeout=30
  local elapsed=0

  while ! mkdir "$lockfile" 2>/dev/null; do
    sleep 0.1
    elapsed=$((elapsed + 1))
    if [ $elapsed -gt $timeout ]; then
      echo "Lock timeout"
      return 1
    fi
  done
  echo $$ > "$lockfile/pid"
  return 0
}

release_lock() {
  rm -rf "plans/${FEATURE}/.taskqueue.lock"
}
```

## Example Run

```bash
$ /ralph "User Authentication" 5

🔧 Setting up Ralph parallel execution environment...
   Found 15 stories across 4 epics
   Detected 8 stories with no dependencies (parallelizable)
   Generated 5 worker scripts

📊 Dependency Map:
   Epic 1: 1.1 → 1.2 → 1.3 (sequential)
   Epic 2: 2.1 → 2.2 (sequential)
   Epic 3: 3.1, 3.2, 3.3 (parallel - no deps!)
   Epic 4: 4.1, 4.2, 4.3 (parallel - no deps!)

🚀 Starting 5 parallel workers...
   [WORKER-1] PID: 12345 - Started
   [WORKER-2] PID: 12346 - Started
   [WORKER-3] PID: 12347 - Started
   [WORKER-4] PID: 12348 - Started
   [WORKER-5] PID: 12349 - Started

📋 Worker Dashboard (refresh every 5s):
   WORKER    STATUS    TASK      COMPLETED    LAST ACTION
   ─────────────────────────────────────────────────────────────
   worker-1  working   1.1       3            Implementing...
   worker-2  working   3.1       2            Testing...
   worker-3  idle      -         4            Waiting for task
   worker-4  working   4.2       1            Reading design...
   worker-5  working   2.1       3            Committing...

   Overall Progress: 13/15 stories (87%)
   Elapsed: 8m 32s

💡 Monitor with:
   tail -f plans/User\ Authentication/progress.txt
   cat plans/User\ Authentication/worker-state.json | jq .

✨ Workers will run until all stories complete.
   To stop: pkill -f "workers/worker-"
```

## Progress Tracking

**`progress.txt`** - Unified progress from all workers
```markdown
# Ralph Progress - User Authentication

## Worker Activity
- Total Workers: 5
- Active: 4, Idle: 1
- Started: 2025-01-15 10:22:00

## Completed Stories

### Story 1.1: Create registration endpoint
- Worker: worker-2
- Completed: 2025-01-15 10:24:15
- Duration: 2m 15s
- Files: src/api/auth.ts, tests/auth.test.ts
- Commit: feat: implement registration endpoint

### Story 3.1: Create user profile model
- Worker: worker-4
- Completed: 2025-01-15 10:23:42
- Duration: 1m 48s
- Files: src/models/User.ts
- Commit: feat: add user profile model

### Story 4.1: Design settings UI
- Worker: worker-1
- Completed: 2025-01-15 10:25:30
- Duration: 3m 05s
- Files: src/components/Settings.tsx, tests/Settings.test.tsx
- Commit: feat: implement settings UI component

## Failed Attempts
### Story 2.2: Payment integration
- Worker: worker-3
- Attempts: 2/10
- Last Error: Stripe API key not configured
- Action: Released to queue, will retry

## Remaining
- Stories: 3
- Est. Time: 6-10 minutes
```

## When All Complete

When all stories are done, workers:
1. Detect empty task queue
2. Verify all tests pass
3. Generate summary report
4. Clean up and exit
5. Output: `<promise>COMPLETE</promise>`

```bash
✨ All workers finished after 18m 42s

📊 Final Statistics:
   Total Stories: 15
   Completed: 15
   Failed: 0
   Retries: 2

👷 Worker Performance:
   worker-1: 4 stories (fastest: 45s per story)
   worker-2: 3 stories (avg: 2m 12s per story)
   worker-3: 3 stories (avg: 2m 45s per story)
   worker-4: 3 stories (avg: 1m 58s per story)
   worker-5: 2 stories (slowest: 3m 30s per story)

🎉 Feature: User Authentication - READY FOR REVIEW
<promise>COMPLETE</promise>
```

## Managing Workers

### Monitor Workers
```bash
# Real-time progress
tail -f plans/{feature}/progress.txt

# Worker status
cat plans/{feature}/worker-state.json | jq '.'

# Task queue status
cat plans/{feature}/task-queue.json | jq '.available | length'
```

### Stop Workers
```bash
# Graceful stop (workers finish current task)
pkill -TERM -f "workers/worker-"

# Immediate stop
pkill -KILL -f "workers/worker-"

# Stop specific worker
pkill -f "workers/worker-3.sh"
```

### Resume After Stop
```bash
# Workers read current state and continue
# No special command needed - just run workers directly
./plans/{feature}/workers/worker-1.sh &
./plans/{feature}/workers/worker-2.sh &
```

## Best Practices

### Choosing Worker Count
```bash
# Rule of thumb: min(#CPU cores, #parallelizable stories)

# CPU with 8 cores, 12 stories
/ralph "Feature" 8

# CPU with 4 cores, 3 stories (mostly sequential deps)
/ralph "Feature" 2

# Large feature with 20+ independent stories
/ralph "Feature" 10
```

### Structuring for Parallelism
```markdown
## Good for Parallelism ✅

### Epic 1: User Service (Backend)
### Story 1.1: User model - No deps
### Story 1.2: Auth service - No deps
### Story 1.3: User controller - No deps

### Epic 2: User UI (Frontend)
### Story 2.1: Login page - No deps
### Story 2.2: Signup page - No deps

→ 5 workers can tackle 1.1, 1.2, 1.3, 2.1, 2.2 simultaneously

## Bad for Parallelism ❌

### Story 1.1: Base model
### Story 1.2: Extends 1.1
### Story 1.3: Extends 1.2

→ Must run sequentially, only 1 worker effective
```

### Sleep Time Tuning
```bash
# Fast network, powerful API → Lower sleep
/ralph "Feature" 5 10 0.5

# Rate limiting concerns → Higher sleep
/ralph "Feature" 5 10 5

# Overnight run → Longer sleep to be safe
/ralph "Feature" 8 20 10
```

## Safety Features

1. **Atomic Locks**: Prevent race conditions on task queue
2. **Heartbeat Monitoring**: Detect stalled workers
3. **Automatic Retry**: Failed tasks return to queue
4. **State Persistence**: Recover from interruption
5. **Test Gates**: No commits without passing tests
6. **Dependency Validation**: Never run tasks with unmet deps

## Document Structure

The breakdown.md should include dependencies for parallel execution:

```markdown
## Epic 1: User Registration

### Story 1.1: Create registration endpoint
**Dependencies**: None
**Estimated**: 2 hours

- [ ] Implement POST /api/auth/register
- [ ] Add input validation
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Write integration tests

### Story 1.2: Email verification
**Dependencies**: Story 1.1 (needs registration endpoint)
**Estimated**: 1.5 hours

- [ ] Implement verification email
- [ ] Add verification endpoint
- [ ] Write tests

## Epic 2: User Profile (can run in parallel with Epic 1)

### Story 2.1: Create profile model
**Dependencies**: None
**Estimated**: 1 hour

- [ ] Define User schema
- [ ] Add database migrations
- [ ] Write model tests
```

Workers will:
- Parse dependencies from each story
- Only claim stories with all dependencies met
- Mark complete `[x]` when done
- Commit after each successful story
- Track progress in `progress.txt`

## Integration with Lifecycle

```
/discover → /prd → /breakdown → /design → /ralph → /review → /test → /release
                                      ↑
                            Parallel autonomous workers
```

## Files Created/Used

```
plans/{feature-name}/
├── breakdown.md         ← Original: tasks with dependencies
├── design.md            ← Original: technical details
├── stories/             ← Original: story-specific designs
│   ├── 1.1.md
│   └── 1.2.md
├── implement.md         ← Original: implementation guidelines
├── task-queue.json      ← CREATED: shared task state
├── worker-state.json    ← CREATED: worker coordination
├── progress.txt         ← CREATED/UPDATED: combined log
└── workers/             ← CREATED: generated worker scripts
    ├── worker-1.sh      ← Each worker is autonomous
    ├── worker-2.sh
    └── worker-N.sh
```

## Tips

### Setup Phase
- Tag dependencies clearly in breakdown.md
- Estimate story complexity for better worker distribution
- Run `/design` on ALL epics before starting `/ralph`
- Ensure tests can run independently (no shared state)

### Worker Configuration
- Start with 3-5 workers for typical features
- Match worker count to CPU cores for CPU-bound tasks
- Use more workers (8-12) for I/O-bound API work
- Fewer workers (1-2) for mostly sequential dependencies

### Monitoring
- Check `task-queue.json` for available vs blocked tasks
- Monitor `worker-state.json` for stalled workers
- Tail `progress.txt` for real-time updates
- Set up alerts for repeated failures on same story

### Performance
- Sleep 0.5-2s for fast APIs with rate limit headroom
- Sleep 5-10s when near rate limits
- Lower iterations (5) for quick tests
- Higher iterations (20+) for overnight runs

## Troubleshooting

### Workers stuck idle?
- Check if all remaining stories have unmet dependencies
- Verify `task-queue.json` has tasks in "available" array
- A dependency might be mislabeled in breakdown.md

### Same story failing repeatedly?
- Check `progress.txt` for error pattern
- Story may have bad design or missing info
- Fix manually, mark `[x]`, let workers continue

### Worker collision issues?
- Increase sleep time to reduce lock contention
- Reduce worker count
- Check that lock file cleanup is working

### Memory issues?
- Reduce worker count
- Workers may need periodic restart (add auto-restart logic)
- Check for leaked processes

## Example Worker Script Output

```
[WORKER-2] Starting...
[WORKER-2] Reading task queue...
[WORKER-2] Found 3 available tasks
[WORKER-2] Acquired lock, claiming task: 1.1
[WORKER-2] Released lock
[WORKER-2] Reading design: plans/User Auth/stories/1.1.md
[WORKER-2] Implementing story: Create registration endpoint
[WORKER-2] Created: src/api/auth.ts
[WORKER-2] Created: src/services/authService.ts
[WORKER-2] Running tests...
[WORKER-2] ✅ 18 tests passed
[WORKER-2] Committing: feat: implement registration endpoint (a1b2c3d)
[WORKER-2] Updating breakdown.md: [x] Story 1.1
[WORKER-2] Acquired lock, marking task complete
[WORKER-2] Checking for next task...
[WORKER-2] Task 1.2 now available (dependency 1.1 met)
[WORKER-2] Acquired lock, claiming task: 1.2
```
