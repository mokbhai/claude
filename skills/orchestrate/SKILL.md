---
name: orchestrate
description: >-
  General-purpose orchestrator that decomposes any task, dispatches autonomous
  headless worker agents in parallel (background) via pluggable CLI adapters
  (agent, claude, cmd, codex, opencode), and reports results when complete. Use this WHENEVER the user wants to fan out work across multiple
  parallel agents, run workers in the background, orchestrate a large task
  across many items or stages, do comprehensive research/audit/analysis/coding
  at scale, or have one coordinator manage many workers. Trigger even if the
  user doesn't say "orchestrate" — phrases like "do this in parallel", "be
  thorough", "comprehensive", "fan this out", "spawn workers", "run agents on
  each of these" all apply. Not coding-specific: works for research, writing,
  analysis, audits, migrations, and anything else.
---

# Orchestrate: parallel worker orchestrator

You are the **coordinator**. You don't do the work yourself — you decompose the
task, hand focused subtasks to autonomous headless CLI workers, run them in
parallel in the background, collect results, verify quality, and report.

Your value is **decomposition, dispatch, and synthesis** — not execution.

Everything runs through **one tool**:

```bash
O=~/.claude/skills/orchestrate/scripts/orchestrator.py
python3 "$O" doctor        # which worker CLIs are installed
python3 "$O" new-run       # create a run dir, prints its path
python3 "$O" batch ...     # dispatch MANY workers in parallel (preferred)
python3 "$O" dispatch ...  # dispatch ONE worker
python3 "$O" status ...    # live table: state, exit, session, output preview
python3 "$O" output ...    # read one worker's clean final answer
```

---

## Engine rule: headless CLI workers first, always

When this skill is active, the dispatch engine is **autonomous headless CLI
workers via `orchestrator.py`** — for *every* fan-out, with no exceptions for
task type. This explicitly includes **read-only research and codebase
understanding**, even though in-harness `Explore`/`Agent` subagents look like
the lighter-touch fit there.

Do **not** substitute `Explore` or the in-harness `Agent` tool as the primary
engine, and do not silently swap engines when the skill is active. If you catch
yourself reasoning "this is just read-only, Explore would be faster/cheaper" —
that's exactly the case this rule overrides. The user has weighed the extra
friction against the benefits and chosen external CLI workers deliberately.

**Why CLI workers are the default even for read-only work:**
- **Durable, auditable artifacts.** Every worker leaves `prompt.txt`,
  `worker.log`, `output.txt`, `session.txt`, and `status.json` on disk —
  re-inspectable later, shareable, and survivable across turns.
- **Structured telemetry.** `status.json` gives exit codes, durations, and
  session ids per task — the substrate real orchestration (retries, scaling,
  blockers) is built on.
- **Context hygiene.** Worker output stays on disk; you read back only the
  clean `output.txt`, not every worker's full stream.
- **One consistent mechanism.** The same engine handles read *and* write work.

**`Explore` is allowed only AFTER CLI workers have run — never before or
instead.** Legitimate follow-up uses: chasing a specific thread a worker
surfaced, a quick targeted lookup to adjudicate a worker's claim, or filling a
narrow gap.

---

## The loop

```
1. DECOMPOSE    break the task into independent subtasks
2. PLAN STAGES  identify if work has multiple stages (pipeline thinking)
3. DISPATCH     one batch manifest per stage, run in background
4. COLLECT      status table + output.txt per worker
5. VERIFY       check quality — retry failures, flag blockers
6. REPORT       summarize results clearly, surface what needs the human
```

---

## Step 0: Setup

```bash
O=~/.claude/skills/orchestrate/scripts/orchestrator.py
RUN_DIR="$(python3 "$O" new-run)"        # .orchestrate/runs/<timestamp>
```

Adapter selection is automatic (first installed among cmd → agent → opencode →
claude → codex). Override per task in the manifest, per dispatch with
`--adapter`, or globally with `WORKER_ADAPTER`. `python3 "$O" doctor` shows
what's installed. See `references/adapters.md` for per-CLI details.

Useful knobs (flags on `dispatch`/`batch`, or per-task manifest keys):

| Knob | Flag / manifest key | Default |
|---|---|---|
| Worker CLI | `--adapter` / `"adapter"` | auto-detect |
| Model override | `--model` / `"model"` | CLI's default |
| Kill runaway worker | `--timeout` / `"timeout"` (seconds, 0 = off, exit 124) | 3600 |
| Turn cap (cmd only) | `--max-turns` / `"max_turns"` | 100 |
| Working directory | `--cwd` / `"cwd"` | current dir |
| Resume a session | `--session <id>` or `--resume-from <task_id>` | fresh |
| Custom CLI | `--worker-cmd 'my-cli "$WORKER_PROMPT"'` | — |

Routing cheap stages (verification votes, formatting) to a smaller model via
`"model"` is an easy cost win on large fan-outs.

---

## Step 1: Decompose

Split the task into **independent subtasks**. Each subtask should be:
- **Focused** — one clear goal, expressible in 1–2 sentences
- **Self-contained** — the worker needs no information it isn't given in the prompt
- **Scoped** — explicit about what it covers and what it doesn't

For each subtask, write down: **id** (short slug), **goal**, **scope**, and
**context** (paste it, don't reference vaguely). If two subtasks depend on each
other's output, they belong in different **stages**, not the same batch.

Write the plan to `$RUN_DIR/plan.md` before dispatching.

---

## Step 2: Pipeline thinking

Most tasks have natural stages where later work depends on earlier results.

**Example: research + verify pipeline**
- Stage 1 batch: gather raw findings on each topic
- Stage 2 batch: verify/cross-check each finding from stage 1
- Stage 3: synthesize verified findings into a report

Within a stage, all workers run in parallel (one manifest). As a stage's
workers finish, build the next stage's manifest from their outputs.

---

## Step 3: Dispatch

**Preferred: one `batch` call per stage.** Write a manifest, launch it in the
background (`run_in_background: true`), and you'll be notified when the whole
stage completes:

```bash
cat > "$RUN_DIR/stage1.json" << 'EOF'
{
  "defaults": {"timeout": 3600},
  "tasks": [
    {"id": "research-auth",  "prompt": "You are an autonomous agent... (full prompt)"},
    {"id": "research-db",    "prompt": "..."},
    {"id": "research-api",   "prompt": "...", "model": "haiku"}
  ]
}
EOF
python3 "$O" batch "$RUN_DIR" "$RUN_DIR/stage1.json" --max-parallel 5
```

`batch` runs tasks concurrently (capped by `--max-parallel`), prints one line
per completion, and exits non-zero if any task failed.

For long prompts, write each to a file and use `"prompt_file"` instead of
`"prompt"` — no escaping headaches.

**Single worker** (odd one-off, or a stage of one — also backgroundable):

```bash
python3 "$O" dispatch "$RUN_DIR" research-auth - << 'EOF'
<full worker prompt>
EOF
```

(`-` reads the prompt from stdin; a file path or `--prompt "text"` also work.)

**Prompt quality matters more than anything.** Each prompt must include:
1. Exactly what to produce and what "done" looks like
2. The precise scope — what it covers and what it doesn't
3. All context it needs, pasted inline (don't say "see the README")
4. Output format — the worker's final printed answer is captured as
   `output.txt`; for large artifacts, have it write files and print a summary

See `references/prompts.md` for reusable templates.

---

## Step 4: Collect

```bash
python3 "$O" status "$RUN_DIR"                # table: state, exit, time, session, preview
python3 "$O" status "$RUN_DIR" --json         # machine-readable
python3 "$O" output "$RUN_DIR" research-auth  # clean final answer
python3 "$O" output "$RUN_DIR" research-auth --log   # raw CLI stream (debugging)
```

Per-task artifacts in `$RUN_DIR/tasks/<task_id>/`:

```
prompt.txt      what the worker was asked
worker.log      raw CLI stream (stdout+stderr)
output.txt      clean final answer (extracted per adapter)
session.txt     session id — resume this worker later
status.json     {task_id, adapter, state, exit_code, duration_s, session_id, ...}
```

A non-zero exit code means the worker errored — treat it as a failed subtask:

| Signal | Meaning | What to do |
|---|---|---|
| exit 0 | Success | Use `output.txt` (still verify quality) |
| exit 1 | General error | Read `worker.log`, retry once if transient |
| Auth failure in log | Not authenticated | Stop — surface to the human (login command in `references/adapters.md`) |
| Rate limit / network | Transient | Wait briefly, re-dispatch — and pause the fan-out, others will hit it too |
| exit 8 | cmd hit `--max-turns` | Re-dispatch with higher `max_turns` or narrower scope |
| exit 124 | Timeout watchdog killed it | Narrower scope or longer `timeout` |
| exit 127 | Worker CLI failed to launch | `python3 "$O" doctor` |

---

## Reusing workers (resumable sessions)

Every completed worker records its session id, so you can send follow-up
messages to a worker that **already has all its context** — no re-pasting:

```bash
python3 "$O" dispatch "$RUN_DIR" build-parser-r2 --resume-from build-parser - << 'EOF'
The parser you wrote chokes on escaped quotes inside strings. Fix that case and
re-run your tests. Tell me what changed.
EOF
```

`--resume-from <task_id>` reads the prior task's `status.json` and reuses its
session id, adapter, and working directory automatically. (In a manifest, use
`"resume_from": "<task_id>"` per task; `--session <raw-id>` also works.)
Resumed runs set `"resumed": true` in `status.json`, so worker lineage stays
auditable. Resume from the same machine/workspace the worker started in.

**When to reuse** — anywhere a cold worker would waste turns rebuilding context:
- **Fix-after-verify.** A verifier flagged problems? Resume the worker that did
  the work and hand it just the issue list.
- **Staged work on one artifact.** Stage 1 drafts; resume for stage 2 (revise,
  extend, harden).
- **Iterative refinement.** Rounds of "now also handle X" on one deliverable.

**When to stay cold (do NOT reuse):**
- **Independent verification.** Verifiers and adversarial skeptics MUST be
  fresh sessions — a worker judging its own work isn't independent.
- **Unrelated subtasks.** Irrelevant history wastes context and can bias.

---

## Step 5: Verify

For each completed subtask, check the output against its goal:
- **Pass** → accept, move to next stage or synthesis
- **Fail, fixable** → resume the original worker (`--resume-from`) with just
  the specific issues. Cap retries at **2**.
- **Fail, blocked** → surface to the human with the worker's log and what was attempted

For high-stakes tasks, run a dedicated **verifier worker** per subtask — an
independent fresh-session agent that checks the output without knowing how it
was produced (batch of verifiers = one manifest).

---

## Step 6: Report

Tell the human:
- What each subtask produced (brief summary per worker)
- Any failures, retries, or blockers — be plain about them
- Where the full outputs live (`$RUN_DIR`)
- What, if anything, needs their decision

"5 of 6 workers completed. Worker `analyze-q3` failed twice on a data format
issue and needs your input. Results in `.orchestrate/runs/20260704-141530/`."
is the right register — honest, specific, actionable.

---

## Scaling patterns

### Many items, one stage
One manifest, one task per item — identical prompt structure, varying only the
item. Generate the manifest programmatically for large item lists:

```bash
python3 - "$RUN_DIR" << 'EOF'
import json, sys
items = ["auth", "billing", "search"]          # your item list
tasks = [{"id": f"audit-{i}", "prompt": f"Audit the {i} module ..."} for i in items]
json.dump({"defaults": {"timeout": 1800}, "tasks": tasks},
          open(f"{sys.argv[1]}/stage1.json", "w"), indent=1)
EOF
python3 "$O" batch "$RUN_DIR" "$RUN_DIR/stage1.json" --max-parallel 8
```

### Loop until dry (unknown-size discovery)
Keep dispatching discovery workers until 2 consecutive rounds surface nothing
new — read each round's `output.txt`, diff against what you've seen, stop when
dry.

### Adversarial verification
For claims that need confidence, batch 3 independent verifiers for the same
claim and require 2/3 agreement. Fresh sessions, never resumed.

---

## Run directory layout

```
.orchestrate/runs/<timestamp>/
├── plan.md                    # decomposition + stage plan (you write this)
├── stage1.json ...            # batch manifests (you write these)
├── tasks/
│   └── <id>/
│       ├── prompt.txt         # saved automatically
│       ├── worker.log         # raw CLI stream
│       ├── output.txt         # clean final answer
│       ├── session.txt        # session id for resume
│       └── status.json        # structured telemetry
└── summary.md                 # final report (you write this)
```

---

## Guardrails

- **CLI workers are the engine — always, even for read-only.** `Explore` is a
  second-pass-only tool (see the engine rule near the top).
- **Workers do the work; you coordinate.** Don't write the output yourself unless
  it's a tiny seam during synthesis.
- **Bound the fan-out.** Know how many workers you're launching before you
  launch them, and set `--max-parallel` deliberately. Match scale to the task.
- **Self-contained prompts.** A worker that has to guess context will produce
  garbage. Paste what it needs.
- **Honest reporting.** Never claim success without reading `output.txt`. Exit
  0 means the process exited cleanly, not that the result is correct.
- **Reuse for continuity, fresh for independence.** `--resume-from` for fixes
  and next stages; fresh sessions for verifiers, skeptics, unrelated work.

---

## References

- `references/adapters.md` — worker CLI adapters (cmd, agent, claude, codex, opencode), verified invocations, login commands
- `references/prompts.md` — reusable worker, verifier, and fix-worker prompt templates
- `scripts/orchestrator.py` — the tool (`--help` on any subcommand)
