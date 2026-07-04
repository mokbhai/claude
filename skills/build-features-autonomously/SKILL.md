---
name: build-features-autonomously
description: >-
  Use WHENEVER the user wants to clear a GitHub backlog, "build out the
  remaining features", "ship issues autonomously", "work through the issues",
  "keep building until there's nothing left", run an unattended dev loop, or
  otherwise hand off feature/bug work to run end-to-end without supervision.
  Trigger even if the user doesn't say "autonomously" — "knock out the open
  issues", "finish the app", "just keep shipping", "open PRs for the backlog"
  all apply.
---

# Build Features Autonomously

You run an **unattended, continuous delivery loop**: take work from the GitHub
issue backlog, ship it through to a reviewed PR, then either act on review
feedback or find the next thing to build — and repeat until there is genuinely
nothing left to do or you hit a real blocker.

You do **not** do the engineering yourself. The **`orchestrate` skill is the
engine** for every substantive phase — understanding the codebase, implementing,
testing, reviewing, simplifying, and reviewing the PR. Invoke the `orchestrate`
skill at the start of each of those phases and let it fan out headless workers.
Your job here is to drive the *outer* loop: sync, select, sequence the phases,
keep state on GitHub, and decide when to stop.

## Operating principles

- **Fully autonomous — never ask the human anything.** If a question or
  ambiguity arises, resolve it yourself, or dispatch a worker (via orchestrate)
  to investigate and decide. Make reasonable, conservative assumptions and keep
  moving. The whole point is that this runs unattended.
- **Orchestrate is the engine.** Each phase below that says "via orchestrate"
  means: invoke the `orchestrate` skill and have it decompose and dispatch
  headless CLI workers. Don't silently substitute doing the work inline — the
  user chose fan-out deliberately.
- **GitHub is the source of truth.** The issue backlog is the work queue and the
  PR is the deliverable. Keep both updated as you go (comments, links, labels) so
  the run is fully auditable after the fact. Do not maintain side files like
  `.unfinished_features/index.md`.
- **Honest reporting and honest state.** Never mark an issue done, claim CI
  passed, or claim a review is clean without reading the actual evidence. A green
  process exit is not the same as a correct result.
- **Preserve the user's work.** Never discard uncommitted changes or force-push
  over history you didn't create. See Phase 0.
- **Document what you ship.** Every PR and every non-trivial code change carries
  clear comments and a description explaining the *why*, not just the *what*.

## Wiring: one run dir per issue cycle

All phases of one issue share **one orchestrate run dir**, so later phases can
resume earlier phases' workers and the whole cycle is auditable in one place:

```bash
O=~/.claude/skills/orchestrate/scripts/orchestrator.py
RUN_DIR=".orchestrate/runs/issue-<number>"          # one per issue cycle
mkdir -p "$RUN_DIR/tasks"
```

- **Task ids carry the phase**: `understand-<area>`, `impl-<part>`,
  `test-<suite>`, `review-diff`, `verify-acceptance`, `simplify-diff`,
  `pr-review-<n>`. `python3 "$O" status "$RUN_DIR"` then reads as a timeline of
  the cycle.
- **Fix = resume, not respawn.** When tests or reviews fail, resume the worker
  that wrote the code: `python3 "$O" dispatch "$RUN_DIR" impl-parser-fix2
  --resume-from impl-parser - <<'EOF' ...`. It works across phases because the
  run dir is shared.
- **Verify = fresh.** Verifiers, reviewers, and skeptics get new task ids with
  no `--resume-from` — independence is the point.
- The run dir is loop-internal state only; GitHub stays the source of truth
  (see operating principles). Don't commit `.orchestrate/` (add to
  `.git/info/exclude` if the repo doesn't ignore it).

## The loop

```
0. SYNC        recover any in-flight cycle, clean worktree safely, sync main
1. SELECT      fetch open issues; pick one. If none, jump to MINE (phase 9)
2. UNDERSTAND  orchestrate: explore the codebase + the issue
3. BRANCH      create a feature branch, comment "starting" on the issue
4. IMPLEMENT   orchestrate: resolve the issue in phases / parallel
5. TEST+REVIEW orchestrate: real UI/API/integration tests + code review
6. SIMPLIFY    orchestrate: verify correctness, simplify the diff
7. SHIP        push branch, open PR, link issue, ensure CI/CD passes
8. PR REVIEW   orchestrate: review the PR, leave a comment, act on feedback
9. MINE        (only when backlog empty) find unfinished work, file issues
→  back to SYNC for the next issue
```

Each numbered phase is detailed below. After Phase 8 finishes for one issue,
return to Phase 0 and start the next. Keep looping until a **stop condition**
(see the end of this file) is met.

---

## Phase 0 — Sync the repository

Always start a cycle from a clean, current `main` — but first, check whether a
**previous cycle was interrupted** and pick it up instead of redoing it:

1. Look for in-flight state from this loop:
   ```bash
   gh pr list --author "@me" --state open --json number,headRefName,title
   git branch --list 'feat/*' 'fix/*'
   ls .orchestrate/runs/ 2>/dev/null    # issue-<n> dirs from prior cycles
   ```
2. If an open PR from this loop exists → resume at **Phase 7 step 4** (watch CI)
   or **Phase 8** (review), whichever it hadn't finished. If a feature branch
   exists with commits but no PR → check out that branch, re-run **Phase 5**
   validation, and continue from there. An issue with a "starting" comment but
   no branch → just restart that issue from Phase 2. Use the branch name /
   run-dir name to recover the issue number, and
   `python3 "$O" status .orchestrate/runs/issue-<n>` to see how far the workers
   got. When in doubt, re-validate rather than trust a stale state.

Then sync:

1. Inspect the worktree: `git status --short --branch`.
2. If there is uncommitted or unmerged work, **preserve it before switching** —
   never discard user changes. Pick the safest option for the state you find:
   finish the in-progress operation (merge/rebase), create a safety branch, make
   an explicit safety commit of your own autonomous work, or
   `git stash push --include-untracked` for clean stashable changes.
3. Switch to main: `git switch main`.
4. Pull latest: `git pull --ff-only origin main`.
5. If `main` doesn't exist locally: `git fetch origin main:main`, then switch and
   pull.
6. Only proceed once `main` is checked out and up to date.

---

## Phase 1 — Select an issue

Treat open GitHub issues as the work queue.

1. Fetch the full open backlog before doing anything else. Prefer the GitHub MCP
   integration if available; otherwise:
   ```bash
   gh issue list --state open --limit 200 \
     --json number,title,body,labels,assignees,url,state,createdAt
   ```
2. Filter to issues that represent genuine unfinished work (skip ones already
   assigned to a human and clearly in progress, unless told otherwise).
3. **If the backlog is empty → go to Phase 9 (Mine)** to generate work, then come
   back here.
4. Otherwise pick **one** issue. Prefer: explicitly prioritized labels (e.g.
   `priority`, `P0`/`P1`), then bugs over features, then smaller well-specified
   issues that can ship cleanly, then oldest. Pick something you can take all the
   way to a PR in one cycle.
5. Note the issue number, title, and acceptance criteria — you'll thread these
   through every later phase.

---

## Phase 2 — Understand (via orchestrate)

Invoke the **`orchestrate` skill** to build a precise understanding before
touching code. Have it fan out workers to:
- Map the parts of the codebase the issue touches (entry points, modules, data
  flow, existing patterns and helpers to reuse).
- Restate the issue as concrete, testable acceptance criteria.
- Identify risks, edge cases, existing tests, and the right validation commands.

Dispatch these as one batch into the cycle's run dir (task ids
`understand-<area>`). Collect the workers' findings (`python3 "$O" output ...`)
into a short implementation plan — what changes, where, in what order, how
it'll be validated — written to `$RUN_DIR/plan.md`. This plan drives Phase 4.

---

## Phase 3 — Branch

1. Create a descriptively named branch off the up-to-date `main`, e.g.
   `git switch -c feat/<issue-number>-<short-slug>` (use `fix/` for bugs).
2. Comment on the issue that work has started, including the branch name, so the
   backlog reflects in-progress state.

---

## Phase 4 — Implement (via orchestrate)

Invoke the **`orchestrate` skill** to resolve the issue against the Phase 2 plan.
- Implement in stages (task ids `impl-<part>`, same run dir); run independent
  parts in parallel, dependent ones as ordered stages. Workers must run with
  `--cwd` set to the repo on the feature branch.
- **Parallel implementers share one working tree** — only parallelize parts
  that touch disjoint files. If parts overlap (same modules, same config,
  generated files), run them as sequential stages instead. Research/read-only
  workers can always run in parallel.
- Reuse existing helpers, shared modules, and established patterns — check before
  adding new abstractions.
- Add **clear comments** for non-obvious logic explaining *why*, matching the
  surrounding code's style and density.
- Keep the change scoped to the issue; don't fold in unrelated refactors.

---

## Phase 5 — Test & review (via orchestrate)

Invoke the **`orchestrate` skill** to validate the change for real.
- Run **real** tests — UI (Playwright CLI where the project supports it), API,
  and integration. No mock-only or "it should work" runs.
- Run the repo's own quality gates (lint, typecheck, targeted tests, and the
  full gate when contracts/build/scripts changed). Read the project's
  CLAUDE.md / AGENTS.md for the exact commands and honor them.
- Run a code review pass over the diff for correctness bugs.
- If anything fails: fix it (resume the implementing worker via
  `--resume-from <its task id>` rather than starting cold) and re-validate. Don't advance
  until tests genuinely pass — and you've read the output confirming it.

---

## Phase 6 — Verify & simplify (via orchestrate)

Invoke the **`orchestrate` skill** to harden and tighten the diff.
- Independently verify the change actually satisfies the acceptance criteria
  (use a **fresh** verifier worker — a worker checking its own work isn't an
  independent check).
- Simplify: remove dead code, collapse duplication, prefer existing helpers,
  drop needless complexity — quality only, without reopening behavior.
- Re-run the relevant validation after simplifying so cleanup didn't regress
  anything.

---

## Phase 7 — Ship the PR

1. Ensure the working tree reflects the validated state, with clear,
   imperative, sentence-case commit messages describing the change.
2. Push the branch: `git push -u origin <branch>`.
3. Open the PR with `gh pr create`, including:
   - A summary of what changed and the **why** behind the approach.
   - Validation performed (which tests/gates ran and their result).
   - `Closes #<issue-number>` to link and auto-close the issue on merge.
4. **Ensure CI/CD passes.** Don't treat opening the PR as done — watch the
   checks:
   ```bash
   gh pr checks <pr-number> --watch
   ```
   If a check fails, read the logs, fix the code/tests on the branch, push, and
   re-watch. Repeat until checks are green. If a check is genuinely
   infrastructure-flaky (not your change), note that in the PR.
5. Comment on the issue with the PR link, validation results, and any remaining
   risks.

---

## Phase 8 — Review the PR & act on feedback (via orchestrate)

After the PR is open and CI is green, invoke the **`orchestrate` skill** to run a
review *of the PR itself*, then act on it.

1. Have orchestrate dispatch reviewer worker(s) over the PR diff looking for
   correctness bugs, missed acceptance criteria, security issues, and obvious
   simplifications. For confidence on risky changes, use multiple independent
   reviewers and weigh agreement.
2. **Leave the review as a comment on the PR** (inline review comments where the
   tooling supports it, e.g. `gh pr review`/`gh pr comment`) so the assessment is
   recorded on GitHub.
3. Triage the findings:
   - **Major bugs or unresolved issues found →** fix them on the branch and
     **push the changes directly to the PR** (it's already your branch). Re-watch
     CI, then re-review until it's clean. Resume the implementing worker for the
     fixes rather than starting cold.
   - **No major issues →** the issue is shipped. Leave a final confirming comment,
     then continue the loop.

A PR is only "done" for the purpose of this loop when CI is green **and** the
review pass found no major bugs or pending issues.

---

## Phase 9 — Mine the codebase for new work (only when the backlog is empty)

Reached only when Phase 1 found no open issues. The goal is to refill the queue
with real, well-scoped work, then resume the loop.

1. Invoke the **`orchestrate` skill** to explore the codebase comprehensively and
   identify unimplemented features, stubs, TODO/FIXME markers, broken or missing
   flows, and gaps against the product's evident intent (README, docs, configs,
   half-built UI). Fan out workers across areas so coverage is broad.
2. Before filing anything, fetch the current open issues again and compare to
   **avoid duplicates** by title, scope, and user-visible behavior.
3. File GitHub issues for each genuine gap:
   - **Group related gaps into a single issue** when they form one coherent unit
     of work.
   - **Split** problems that are unrelated, or too large to finish in one cycle,
     into **multiple sequential issues** sized to ship cleanly one at a time.
   - Each issue body: goal, expected behavior, acceptance criteria, likely
     touched areas, and validation notes. Add labels the repo already uses.
4. If an existing issue turns out to be already implemented, comment with the
   validation evidence and close it.
5. Refresh the backlog, then **return to Phase 1** and address the first new
   issue — implement, test, review, simplify, push, PR, ensure CI passes, then
   run the Phase 8 PR review and act on its feedback. The loop continues exactly
   as before.

---

## Stop conditions

Keep looping until one of these is true, then report:

- **Backlog empty and mining finds nothing new** for two consecutive rounds —
  the project is genuinely complete for now.
- **A hard blocker** you cannot resolve autonomously: missing credentials/auth
  for the worker CLI or `gh`, a repository you lack push access to, a failing
  gate that requires a human decision (e.g. an intentional contract break), or
  repeated worker failures after retries.
- **Repeated CI or review failures** on the same PR after 2–3 honest fix attempts
  — surface it rather than thrashing.

When you stop, report plainly: issues shipped (with PR links), PRs awaiting human
merge, anything skipped and why, and any blocker that needs the human. Be
specific and honest — the value of an unattended loop is a trustworthy summary at
the end.

---

## Guardrails

- **One issue in flight at a time.** Finish a cycle (through Phase 8) before
  starting the next, so each PR stays clean and reviewable.
- **Don't merge unless told to.** Open PRs and get them green and reviewed;
  leave the merge decision to the human unless the user explicitly authorized
  auto-merge.
- **Respect the repo's rules.** Read CLAUDE.md / AGENTS.md and follow its build,
  test, commit, and PR conventions exactly — they override the generic commands
  here.
- **Never fabricate green.** Read CI output and review output before claiming
  either passed. If you didn't verify it, say so.
