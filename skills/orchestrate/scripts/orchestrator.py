#!/usr/bin/env python3
"""orchestrator.py — dispatch and manage headless CLI worker agents.

One tool, five adapters (cmd, agent, opencode, claude, codex), uniform artifacts.

Subcommands:
  new-run                 create a fresh run directory and print its path
  dispatch                run ONE worker (synchronous; background it yourself)
  batch                   run MANY workers from a JSON manifest, in parallel
  status                  table of every task in a run (state, exit, output)
  output                  print a task's clean output (or raw log with --log)
  doctor                  show which worker CLIs are installed

Per-task artifacts in <run_dir>/tasks/<task_id>/:
  prompt.txt    the prompt the worker received
  worker.log    raw CLI stream (stdout+stderr)
  output.txt    clean final answer (extracted per adapter)
  session.txt   session id for resuming this worker
  status.json   {task_id, adapter, state, exit_code, session_id, ...}

Environment defaults (flags win): WORKER_ADAPTER, WORKER_MODEL, WORKER_SESSION,
WORKER_TIMEOUT, WORKER_MAX_TURNS, WORKER_CMD, CMD_PROJECTS_DIR.

Exit codes: worker's own exit code; 124 = timeout; 2 = usage/setup error.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

AUTO_ORDER = ["cmd", "agent", "opencode", "claude", "codex"]
DEFAULT_TIMEOUT = 3600
DEFAULT_MAX_TURNS = 100


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def die(msg, code=2):
    print(f"orchestrator: {msg}", file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------- adapters

def _last_json_object(text):
    """Return the last line of text that parses as a JSON object, else None."""
    for line in reversed(text.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def build_claude(ctx):
    argv = ["claude", "-p", "--dangerously-skip-permissions",
            "--output-format", "json"]
    if ctx["session"]:
        argv += ["--resume", ctx["session"]]
    else:
        ctx["session_hint"] = str(uuid.uuid4())
        argv += ["--session-id", ctx["session_hint"]]
    if ctx["model"]:
        argv += ["--model", ctx["model"]]
    return argv, ctx["prompt"]


def extract_claude(ctx, log_text):
    obj = _last_json_object(log_text)
    if obj and "result" in obj:
        return obj.get("session_id") or ctx.get("session_hint"), obj["result"]
    return ctx.get("session_hint"), None


def build_agent(ctx):
    argv = ["agent", "--yolo", "-p", "--trust", "--output-format", "json"]
    if ctx["session"]:
        argv += ["--resume", ctx["session"]]
    if ctx["model"]:
        argv += ["--model", ctx["model"]]
    return argv, ctx["prompt"]


def extract_agent(ctx, log_text):
    obj = _last_json_object(log_text)
    if obj and "result" in obj:
        return obj.get("session_id"), obj["result"]
    return None, None


def build_cmd(ctx):
    argv = ["cmd", "-p", "--yolo", "--trust", "--skip-onboarding",
            "--max-turns", str(ctx["max_turns"])]
    if ctx["session"]:
        argv += ["-r", ctx["session"]]
    if ctx["model"]:
        argv += ["-m", ctx["model"]]
    return argv, ctx["prompt"]


def _cmd_projects_root():
    return Path(os.environ.get("CMD_PROJECTS_DIR",
                               Path.home() / ".commandcode" / "projects"))


def _cmd_slug(cwd):
    return re.sub(r"[^a-z0-9]+", "-", str(cwd).lower()).strip("-")


def _cmd_first_user_content(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for _ in range(50):
                line = fh.readline()
                if not line:
                    break
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue
                if obj.get("role") == "user":
                    content = obj.get("content")
                    if isinstance(content, list):
                        content = " ".join(p.get("text", "") for p in content
                                           if isinstance(p, dict))
                    return content if isinstance(content, str) else ""
    except OSError:
        pass
    return None


def extract_cmd(ctx, log_text):
    """Session id = the new <uuid>.jsonl that appeared in cmd's per-project
    transcript dir during the run and whose first user message is our prompt."""
    output = log_text.strip() or None
    if ctx["session"]:
        return ctx["session"], output
    root = _cmd_projects_root()
    project_dir = root / _cmd_slug(ctx["cwd"])
    search_dirs = [project_dir] if project_dir.is_dir() else \
        [d for d in root.iterdir() if d.is_dir()] if root.is_dir() else []
    prompt_head = ctx["prompt"].strip()[:200]
    candidates = []
    for d in search_dirs:
        for f in d.glob("*.jsonl"):
            if f.name.endswith(".checkpoints.jsonl"):
                continue
            try:
                mtime = f.stat().st_mtime
            except OSError:
                continue
            if mtime < ctx["start_time"] - 2:
                continue
            first_user = _cmd_first_user_content(f)
            if first_user is None:
                continue
            if first_user.strip()[:200] == prompt_head:
                candidates.append((mtime, f.stem))
    candidates.sort()
    return (candidates[-1][1] if candidates else None), output


def build_codex(ctx):
    argv = ["codex", "exec", "--skip-git-repo-check",
            "--dangerously-bypass-approvals-and-sandbox",
            "-o", str(ctx["task_dir"] / "output.txt")]
    if ctx["model"]:
        argv += ["-m", ctx["model"]]
    if ctx["session"]:
        argv += ["resume", ctx["session"]]
    argv += ["-"]
    return argv, ctx["prompt"]


def extract_codex(ctx, log_text):
    if ctx["session"]:
        session = ctx["session"]
    else:
        m = re.search(r"session id:\s*([0-9a-f][0-9a-f-]+)", log_text)
        session = m.group(1) if m else None
    out_file = ctx["task_dir"] / "output.txt"
    output = out_file.read_text(encoding="utf-8",
                                errors="replace").strip() if out_file.is_file() else None
    return session, output


def build_opencode(ctx):
    argv = ["opencode", "run", "--dangerously-skip-permissions",
            "--format", "json", "--title", ctx["task_id"]]
    if ctx["session"]:
        argv += ["--session", ctx["session"]]
    if ctx["model"]:
        argv += ["--model", ctx["model"]]
    argv += [ctx["prompt"]]
    return argv, None


def extract_opencode(ctx, log_text):
    session = ctx["session"]
    texts = []
    for line in log_text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        session = session or obj.get("sessionID")
        part = obj.get("part")
        if isinstance(part, dict):
            session = session or part.get("sessionID")
            if part.get("type") == "text" and part.get("text"):
                texts.append(part["text"])
    return session, ("\n".join(texts).strip() or None)


ADAPTERS = {
    "cmd": {"name": "Command Code", "login": "cmd login",
            "build": build_cmd, "extract": extract_cmd},
    "agent": {"name": "Cursor Agent", "login": "agent login",
              "build": build_agent, "extract": extract_agent},
    "opencode": {"name": "OpenCode", "login": "opencode auth login",
                 "build": build_opencode, "extract": extract_opencode},
    "claude": {"name": "Claude Code", "login": "claude (sign in on first run)",
               "build": build_claude, "extract": extract_claude},
    "codex": {"name": "Codex", "login": "codex login",
              "build": build_codex, "extract": extract_codex},
}


def resolve_adapter(requested):
    requested = requested or "auto"
    if requested == "auto":
        order = os.environ.get("WORKER_ADAPTER_AUTO_ORDER", " ".join(AUTO_ORDER)).split()
        for candidate in order:
            if candidate in ADAPTERS and shutil.which(candidate):
                return candidate
        die(f"no worker CLI found in PATH (tried: {' '.join(order)})")
    if requested not in ADAPTERS:
        die(f"unknown adapter '{requested}' (known: {', '.join(ADAPTERS)}, auto)")
    if not shutil.which(requested):
        die(f"adapter '{requested}' requested but '{requested}' not found in PATH "
            f"(login/install: {ADAPTERS[requested]['login']})")
    return requested


# ---------------------------------------------------------------- dispatch

def write_status(task_dir, payload):
    tmp = task_dir / "status.json.tmp"
    tmp.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    tmp.replace(task_dir / "status.json")


def run_worker(run_dir, task_id, prompt, adapter=None, model=None, session=None,
               resume_from=None, timeout=None, max_turns=None, cwd=None,
               worker_cmd=None):
    """Run one worker to completion. Returns the final status dict."""
    run_dir = Path(run_dir)
    task_dir = run_dir / "tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    if resume_from:
        prior = run_dir / "tasks" / resume_from / "status.json"
        if not prior.is_file():
            die(f"--resume-from: no status.json for task '{resume_from}' in {run_dir}")
        prior_status = json.loads(prior.read_text(encoding="utf-8"))
        if not prior_status.get("session_id"):
            die(f"--resume-from: task '{resume_from}' has no captured session id")
        session = prior_status["session_id"]
        adapter = adapter or prior_status.get("adapter")
        cwd = cwd or prior_status.get("cwd")

    cwd = str(Path(cwd).resolve()) if cwd else os.getcwd()
    timeout = DEFAULT_TIMEOUT if timeout is None else timeout
    max_turns = max_turns or DEFAULT_MAX_TURNS

    if worker_cmd:
        adapter_id = "custom"
        argv = ["bash", "-c", worker_cmd]
        stdin_text = None
    else:
        adapter_id = resolve_adapter(adapter)

    (task_dir / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")

    ctx = {"run_dir": run_dir, "task_dir": task_dir, "task_id": task_id,
           "prompt": prompt, "model": model, "session": session,
           "max_turns": max_turns, "cwd": cwd, "start_time": time.time()}

    status = {"task_id": task_id, "adapter": adapter_id, "state": "running",
              "exit_code": None, "timed_out": False, "duration_s": None,
              "started_at": now_iso(), "ended_at": None,
              "session_id": session, "resumed": bool(session),
              "model": model, "cwd": cwd, "error": None}
    write_status(task_dir, status)

    if not worker_cmd:
        argv, stdin_text = ADAPTERS[adapter_id]["build"](ctx)

    env = dict(os.environ)
    if worker_cmd:
        env["WORKER_PROMPT"] = prompt

    log_path = task_dir / "worker.log"
    ctx["start_time"] = start = time.time()
    timed_out = False
    with open(log_path, "wb") as log_fh:
        try:
            proc = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
                stdout=log_fh, stderr=subprocess.STDOUT,
                cwd=cwd, env=env, start_new_session=True)
        except OSError as exc:
            status.update(state="done", exit_code=127, ended_at=now_iso(),
                          duration_s=0, error=f"failed to launch: {exc}")
            write_status(task_dir, status)
            return status

        if stdin_text is not None:
            def _feed():
                try:
                    proc.stdin.write(stdin_text.encode("utf-8"))
                    proc.stdin.close()
                except (BrokenPipeError, OSError):
                    pass
            threading.Thread(target=_feed, daemon=True).start()

        try:
            code = proc.wait(timeout=timeout if timeout and timeout > 0 else None)
        except subprocess.TimeoutExpired:
            timed_out = True
            code = 124
            try:
                os.killpg(proc.pid, 15)
                proc.wait(timeout=10)
            except (subprocess.TimeoutExpired, ProcessLookupError, PermissionError):
                try:
                    os.killpg(proc.pid, 9)
                except (ProcessLookupError, PermissionError):
                    pass
                proc.wait()

    log_text = log_path.read_text(encoding="utf-8", errors="replace")
    session_id, output = (session, None) if worker_cmd else \
        ADAPTERS[adapter_id]["extract"](ctx, log_text)
    session_id = session_id or session

    (task_dir / "session.txt").write_text((session_id or "") + "\n", encoding="utf-8")
    if output:
        (task_dir / "output.txt").write_text(output + "\n", encoding="utf-8")

    status.update(state="done", exit_code=code, timed_out=timed_out,
                  duration_s=round(time.time() - start, 1),
                  ended_at=now_iso(), session_id=session_id)
    if timed_out:
        status["error"] = f"timed out after {timeout}s"
    write_status(task_dir, status)
    return status


def summarize_line(status):
    sid = (status.get("session_id") or "-")[:8]
    dur = status.get("duration_s")
    dur = f"{dur:.0f}s" if isinstance(dur, (int, float)) else "-"
    flag = " TIMEOUT" if status.get("timed_out") else ""
    return (f"{status['task_id']}: adapter={status['adapter']} "
            f"exit={status.get('exit_code')} time={dur} session={sid}{flag}")


# ---------------------------------------------------------------- commands

def read_prompt(source, inline):
    if inline is not None:
        return inline
    if source in (None, "-"):
        text = sys.stdin.read()
    else:
        path = Path(source)
        if not path.is_file():
            die(f"prompt file not found: {source}")
        text = path.read_text(encoding="utf-8")
    if not text.strip():
        die("prompt is empty")
    return text


def cmd_dispatch(args):
    prompt = read_prompt(args.prompt_src, args.prompt)
    status = run_worker(
        args.run_dir, args.task_id, prompt,
        adapter=args.adapter, model=args.model, session=args.session,
        resume_from=args.resume_from, timeout=args.timeout,
        max_turns=args.max_turns, cwd=args.cwd, worker_cmd=args.worker_cmd)
    print(summarize_line(status))
    if status.get("exit_code") != 0:
        print(f"  see: {Path(args.run_dir) / 'tasks' / args.task_id / 'worker.log'}",
              file=sys.stderr)
    sys.exit(status.get("exit_code") or 0)


def cmd_batch(args):
    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        die(f"manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    defaults = manifest.get("defaults", {})
    tasks = manifest.get("tasks", [])
    if not tasks:
        die("manifest has no tasks")
    seen = set()
    for t in tasks:
        if not t.get("id"):
            die("every task needs an 'id'")
        if t["id"] in seen:
            die(f"duplicate task id '{t['id']}'")
        seen.add(t["id"])
        if not t.get("prompt") and not t.get("prompt_file"):
            die(f"task '{t['id']}' needs 'prompt' or 'prompt_file'")

    def opt(task, key, fallback=None):
        return task.get(key, defaults.get(key, fallback))

    def run_one(task):
        prompt = task.get("prompt") or Path(task["prompt_file"]).read_text(encoding="utf-8")
        return run_worker(
            args.run_dir, task["id"], prompt,
            adapter=opt(task, "adapter", args.adapter),
            model=opt(task, "model"),
            session=task.get("session"),
            resume_from=task.get("resume_from"),
            timeout=opt(task, "timeout", args.timeout),
            max_turns=opt(task, "max_turns"),
            cwd=opt(task, "cwd"))

    results = []
    done = 0
    with ThreadPoolExecutor(max_workers=args.max_parallel) as pool:
        futures = {pool.submit(run_one, t): t["id"] for t in tasks}
        for future in as_completed(futures):
            done += 1
            status = future.result()
            results.append(status)
            print(f"[{done}/{len(tasks)}] {summarize_line(status)}", flush=True)

    failed = [s for s in results if s.get("exit_code") != 0]
    print(f"\nbatch: {len(results) - len(failed)}/{len(results)} succeeded"
          + (f", {len(failed)} FAILED: {', '.join(s['task_id'] for s in failed)}"
             if failed else ""))
    sys.exit(1 if failed else 0)


def load_statuses(run_dir):
    tasks_dir = Path(run_dir) / "tasks"
    if not tasks_dir.is_dir():
        die(f"no tasks directory in {run_dir}")
    statuses = []
    for task_dir in sorted(tasks_dir.iterdir()):
        status_file = task_dir / "status.json"
        if status_file.is_file():
            try:
                statuses.append(json.loads(status_file.read_text(encoding="utf-8")))
            except ValueError:
                statuses.append({"task_id": task_dir.name, "state": "corrupt"})
    return statuses


def cmd_status(args):
    statuses = load_statuses(args.run_dir)
    if args.json:
        print(json.dumps(statuses, indent=2))
        return
    if not statuses:
        print("no tasks yet")
        return
    rows = []
    for s in statuses:
        out_file = Path(args.run_dir) / "tasks" / s.get("task_id", "") / "output.txt"
        preview = ""
        if out_file.is_file():
            preview = " ".join(out_file.read_text(encoding="utf-8",
                                                  errors="replace").split())[:60]
        exit_code = s.get("exit_code")
        state = s.get("state", "?")
        if s.get("timed_out"):
            state = "timeout"
        elif state == "done":
            state = "ok" if exit_code == 0 else f"FAIL({exit_code})"
        dur = s.get("duration_s")
        rows.append((s.get("task_id", "?"), s.get("adapter", "?"), state,
                     f"{dur:.0f}s" if isinstance(dur, (int, float)) else "-",
                     (s.get("session_id") or "-")[:8], preview))
    headers = ("TASK", "ADAPTER", "STATE", "TIME", "SESSION", "OUTPUT")
    widths = [max(len(headers[i]), *(len(r[i]) for r in rows)) for i in range(5)]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths) + "  {}"
    print(fmt.format(*headers))
    for row in rows:
        print(fmt.format(*row))
    ok = sum(1 for s in statuses if s.get("state") == "done" and s.get("exit_code") == 0)
    running = sum(1 for s in statuses if s.get("state") == "running")
    print(f"\n{ok}/{len(statuses)} ok, {running} running, "
          f"{len(statuses) - ok - running} failed")


def cmd_output(args):
    task_dir = Path(args.run_dir) / "tasks" / args.task_id
    output_file = task_dir / "output.txt"
    log_file = task_dir / "worker.log"
    if not args.log and output_file.is_file():
        sys.stdout.write(output_file.read_text(encoding="utf-8", errors="replace"))
    elif log_file.is_file():
        sys.stdout.write(log_file.read_text(encoding="utf-8", errors="replace"))
    else:
        die(f"no output for task '{args.task_id}' in {args.run_dir}")


def cmd_new_run(args):
    root = Path(args.root)
    run_dir = root / time.strftime("%Y%m%d-%H%M%S")
    suffix = 0
    while run_dir.exists():
        suffix += 1
        run_dir = root / f"{time.strftime('%Y%m%d-%H%M%S')}-{suffix}"
    (run_dir / "tasks").mkdir(parents=True)
    print(run_dir)


def cmd_doctor(_args):
    print(f"{'ADAPTER':<10}{'CLI':<42}LOGIN")
    for adapter_id, spec in ADAPTERS.items():
        path = shutil.which(adapter_id) or "NOT INSTALLED"
        print(f"{adapter_id:<10}{path:<42}{spec['login']}")


# ---------------------------------------------------------------- main

def env_int(name):
    value = os.environ.get(name)
    return int(value) if value and value.isdigit() else None


def main():
    parser = argparse.ArgumentParser(
        prog="orchestrator.py",
        description="Dispatch and manage headless CLI worker agents.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("new-run", help="create a fresh run directory, print its path")
    p.add_argument("--root", default=".orchestrate/runs")
    p.set_defaults(func=cmd_new_run)

    p = sub.add_parser("dispatch", help="run one worker synchronously")
    p.add_argument("run_dir")
    p.add_argument("task_id")
    p.add_argument("prompt_src", nargs="?", default="-",
                   help="prompt file, or '-' for stdin (default)")
    p.add_argument("--prompt", help="inline prompt text (instead of file/stdin)")
    p.add_argument("--adapter", default=os.environ.get("WORKER_ADAPTER"),
                   help="cmd|agent|opencode|claude|codex|auto")
    p.add_argument("--model", default=os.environ.get("WORKER_MODEL") or None)
    p.add_argument("--session", default=os.environ.get("WORKER_SESSION") or None,
                   help="resume this session id")
    p.add_argument("--resume-from", metavar="TASK_ID",
                   help="resume the session of a prior task in this run")
    p.add_argument("--timeout", type=int, default=env_int("WORKER_TIMEOUT"))
    p.add_argument("--max-turns", type=int, default=env_int("WORKER_MAX_TURNS"))
    p.add_argument("--cwd", help="working directory for the worker")
    p.add_argument("--worker-cmd", default=os.environ.get("WORKER_CMD") or None,
                   help="bypass adapters: shell command, prompt in $WORKER_PROMPT")
    p.set_defaults(func=cmd_dispatch)

    p = sub.add_parser("batch", help="run many workers from a JSON manifest")
    p.add_argument("run_dir")
    p.add_argument("manifest", help='{"defaults":{...},"tasks":[{"id","prompt",...}]}')
    p.add_argument("--max-parallel", type=int, default=5)
    p.add_argument("--adapter", default=os.environ.get("WORKER_ADAPTER"))
    p.add_argument("--timeout", type=int, default=env_int("WORKER_TIMEOUT"))
    p.set_defaults(func=cmd_batch)

    p = sub.add_parser("status", help="show all tasks in a run")
    p.add_argument("run_dir")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("output", help="print a task's clean output")
    p.add_argument("run_dir")
    p.add_argument("task_id")
    p.add_argument("--log", action="store_true", help="print raw worker.log instead")
    p.set_defaults(func=cmd_output)

    p = sub.add_parser("doctor", help="show installed worker CLIs")
    p.set_defaults(func=cmd_doctor)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
