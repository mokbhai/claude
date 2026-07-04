# Worker CLI adapters

`orchestrator.py` dispatches autonomous workers through **adapters** — one per
headless coding-agent CLI, all implemented inside `scripts/orchestrator.py`.
Selection is per task (`"adapter"` in a manifest, `--adapter` on dispatch),
via `WORKER_ADAPTER`, or automatic (first installed wins).

## Selection

```bash
python3 "$O" doctor                  # show installed CLIs + login commands

--adapter auto                       # default — probe order: cmd agent opencode claude codex
--adapter cmd|agent|opencode|claude|codex

export WORKER_ADAPTER=claude         # env default (flags win)
export WORKER_ADAPTER_AUTO_ORDER="claude cmd agent codex opencode"   # reorder auto probe
```

`status.json` records which adapter ran (`"adapter": "claude"`).

## Verified invocations

Every row below was executed and verified on 2026-07-04.

| Adapter | Fresh run | Resume | Session id source | Clean output source |
|---|---|---|---|---|
| `cmd` (Command Code) | `cmd -p --yolo --trust --skip-onboarding --max-turns N` (prompt on stdin) | `-r <id>` | new `<id>.jsonl` in `~/.commandcode/projects/<cwd-slug>/`, matched by prompt | stdout (already clean) |
| `agent` (Cursor) | `agent --yolo -p --trust --output-format json` (prompt on stdin) | `--resume <id>` | `session_id` in JSON result | `result` in JSON result |
| `opencode` | `opencode run --dangerously-skip-permissions --format json --title <task>` (prompt as arg) | `--session <id>` | `sessionID` in JSON events | text parts in JSON events |
| `claude` (Claude Code) | `claude -p --dangerously-skip-permissions --output-format json --session-id <uuid>` (prompt on stdin) | `--resume <id>` | pre-generated uuid, confirmed in JSON result | `result` in JSON result |
| `codex` | `codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -o output.txt -` (prompt on stdin) | `... resume <id> -` | `session id:` line in header | `-o` last-message file |

Model overrides: `cmd -m`, `agent --model`, `opencode --model`, `claude
--model`, `codex -m` — all wired to `--model` / `"model"`.

Turn cap: only `cmd` supports one (`--max-turns`, default 100, exit 8 on
cap-hit) — wired to `--max-turns` / `"max_turns"`.

## Login / auth

| Adapter | Login |
|---|---|
| `cmd` | `cmd login` |
| `agent` | `agent login` |
| `opencode` | `opencode auth login` |
| `claude` | run `claude` once and sign in |
| `codex` | `codex login` |

An auth failure shows up as a non-zero exit with an auth error in
`worker.log`. Stop and surface the login command to the human — workers can't
authenticate themselves.

## Custom CLI (bypass adapters)

```bash
python3 "$O" dispatch "$RUN_DIR" my-task --worker-cmd 'my-cli --headless "$WORKER_PROMPT"' - << 'EOF'
<prompt>
EOF
```

The prompt is exported as `$WORKER_PROMPT`. No session capture — pass
`--session` yourself if your CLI supports resume.

## Adding an adapter

Adapters live in `scripts/orchestrator.py` as a `build_<name>(ctx)` /
`extract_<name>(ctx, log_text)` pair registered in `ADAPTERS`:

1. `build` returns `(argv, stdin_text_or_None)`. Read `ctx["session"]`
   (resume id or None), `ctx["model"]`, `ctx["max_turns"]`, `ctx["task_dir"]`.
2. `extract` runs after the process exits; return `(session_id, clean_output)`
   — either may be None. It gets the full `worker.log` text.
3. Register in `ADAPTERS` and add the id to `AUTO_ORDER` if it should be
   auto-probed. Update this doc's tables.

Verify with a real run before documenting:
`python3 "$O" dispatch /tmp/run t1 --adapter <name> --prompt "Reply with exactly: PING"`.
