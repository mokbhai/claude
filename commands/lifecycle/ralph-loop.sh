#!/usr/bin/env bash
# Ralph Loop - Autonomous Implementation for Claude Code Lifecycle
# Enhanced with parallel execution, git worktrees, and multiple AI engine support
# Usage: ./ralph-loop.sh <feature-name> [options]

set -euo pipefail

# ============================================
# CONFIGURATION & DEFAULTS
# ============================================

VERSION="2.0.0"

# Runtime options
SKIP_TESTS=false
SKIP_LINT=false
AI_ENGINE="claude"  # claude, opencode, cursor, or codex
DRY_RUN=false
MAX_ITERATIONS=0  # 0 = unlimited
MAX_RETRIES=3
RETRY_DELAY=5
VERBOSE=false

# Git branch options
BRANCH_PER_TASK=false
CREATE_PR=false
BASE_BRANCH=""
PR_DRAFT=false

# Parallel execution
PARALLEL=false
MAX_PARALLEL=3

# Colors (detect if terminal supports colors)
if [[ -t 1 ]] && command -v tput &>/dev/null && [[ $(tput colors 2>/dev/null || echo 0) -ge 8 ]]; then
  RED=$(tput setaf 1)
  GREEN=$(tput setaf 2)
  YELLOW=$(tput setaf 3)
  BLUE=$(tput setaf 4)
  MAGENTA=$(tput setaf 5)
  CYAN=$(tput setaf 6)
  BOLD=$(tput bold)
  DIM=$(tput dim)
  RESET=$(tput sgr0)
else
  RED="" GREEN="" YELLOW="" BLUE="" MAGENTA="" CYAN="" BOLD="" DIM="" RESET=""
fi

# Global state
ai_pid=""
monitor_pid=""
tmpfile=""
CODEX_LAST_MESSAGE_FILE=""
current_step="Thinking"
total_input_tokens=0
total_output_tokens=0
total_actual_cost="0"
total_duration_ms=0
iteration=0
retry_count=0
declare -a parallel_pids=()
declare -a task_branches=()
WORKTREE_BASE=""
ORIGINAL_DIR=""

# ============================================
# UTILITY FUNCTIONS
# ============================================

log_info() {
  echo "${BLUE}[INFO]${RESET} $*"
}

log_success() {
  echo "${GREEN}[OK]${RESET} $*"
}

log_warn() {
  echo "${YELLOW}[WARN]${RESET} $*"
}

log_error() {
  echo "${RED}[ERROR]${RESET} $*" >&2
}

log_debug() {
  if [[ "$VERBOSE" == true ]]; then
    echo "${DIM}[DEBUG] $*${RESET}"
  fi
}

# Slugify text for branch names
slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-|-$//g' | cut -c1-50
}

# ============================================
# HELP & VERSION
# ============================================

show_help() {
  cat << EOF
${BOLD}Ralph Loop${RESET} - Autonomous Implementation Loop (v${VERSION})

${BOLD}USAGE:${RESET}
  ./ralph-loop.sh <feature-name> [options]

${BOLD}AI ENGINE OPTIONS:${RESET}
  --claude            Use Claude Code (default)
  --opencode          Use OpenCode
  --cursor            Use Cursor agent
  --codex             Use Codex CLI

${BOLD}WORKFLOW OPTIONS:${RESET}
  --no-tests          Skip writing and running tests
  --no-lint           Skip linting
  --fast              Skip both tests and linting

${BOLD}EXECUTION OPTIONS:${RESET}
  --max-iterations N  Stop after N iterations (0 = unlimited)
  --max-retries N     Max retries per task on failure (default: 3)
  --retry-delay N     Seconds between retries (default: 5)
  --dry-run           Show what would be done without executing

${BOLD}PARALLEL EXECUTION:${RESET}
  --parallel          Run independent tasks in parallel
  --max-parallel N    Max concurrent tasks (default: 3)

${BOLD}GIT BRANCH OPTIONS:${RESET}
  --branch-per-task   Create a new git branch for each task
  --base-branch NAME  Base branch to create task branches from (default: current)
  --create-pr         Create a pull request after each task (requires gh CLI)
  --draft-pr          Create PRs as drafts

${BOLD}OTHER OPTIONS:${RESET}
  -v, --verbose       Show debug output
  -h, --help          Show this help
  --version           Show version number

${BOLD}EXAMPLES:${RESET}
  ./ralph-loop.sh "User Authentication"
  ./ralph-loop.sh "User Authentication" --parallel --max-parallel 4
  ./ralph-loop.sh "User Authentication" --branch-per-task --create-pr
  ./ralph-loop.sh "User Authentication" --fast --max-iterations 20

EOF
}

show_version() {
  echo "Ralph Loop v${VERSION}"
}

# ============================================
# ARGUMENT PARSING
# ============================================

FEATURE_NAME=""

parse_args() {
  # Handle --help and --version first (before requiring feature name)
  if [[ $# -gt 0 ]]; then
    case "$1" in
      -h|--help)
        show_help
        exit 0
        ;;
      --version)
        show_version
        exit 0
        ;;
    esac
  fi

  if [[ $# -eq 0 ]]; then
    show_help
    exit 1
  fi

  FEATURE_NAME="${1}"
  shift

  while [[ $# -gt 0 ]]; do
    case $1 in
      --no-tests|--skip-tests)
        SKIP_TESTS=true
        shift
        ;;
      --no-lint|--skip-lint)
        SKIP_LINT=true
        shift
        ;;
      --fast)
        SKIP_TESTS=true
        SKIP_LINT=true
        shift
        ;;
      --opencode)
        AI_ENGINE="opencode"
        shift
        ;;
      --claude)
        AI_ENGINE="claude"
        shift
        ;;
      --cursor|--agent)
        AI_ENGINE="cursor"
        shift
        ;;
      --codex)
        AI_ENGINE="codex"
        shift
        ;;
      --dry-run)
        DRY_RUN=true
        shift
        ;;
      --max-iterations)
        MAX_ITERATIONS="${2:-0}"
        shift 2
        ;;
      --max-retries)
        MAX_RETRIES="${2:-3}"
        shift 2
        ;;
      --retry-delay)
        RETRY_DELAY="${2:-5}"
        shift 2
        ;;
      --parallel)
        PARALLEL=true
        shift
        ;;
      --max-parallel)
        MAX_PARALLEL="${2:-3}"
        shift 2
        ;;
      --branch-per-task)
        BRANCH_PER_TASK=true
        shift
        ;;
      --base-branch)
        BASE_BRANCH="${2:-}"
        shift 2
        ;;
      --create-pr)
        CREATE_PR=true
        shift
        ;;
      --draft-pr)
        PR_DRAFT=true
        shift
        ;;
      -v|--verbose)
        VERBOSE=true
        shift
        ;;
      *)
        log_error "Unknown option: $1"
        echo "Use --help for usage"
        exit 1
        ;;
    esac
  done
}

# ============================================
# PRE-FLIGHT CHECKS
# ============================================

check_requirements() {
  PLANS_DIR="plans/${FEATURE_NAME}"

  if [[ -z "$FEATURE_NAME" ]]; then
    log_error "Feature name required"
    exit 1
  fi

  if [[ ! -d "$PLANS_DIR" ]]; then
    log_error "Plans directory not found: $PLANS_DIR"
    log_error "Please run /breakdown first to create the plan structure"
    exit 1
  fi

  # Check for breakdown.md
  if [[ ! -f "$PLANS_DIR/breakdown.md" ]]; then
    log_error "breakdown.md not found in $PLANS_DIR"
    exit 1
  fi

  # Check for AI CLI
  case "$AI_ENGINE" in
    opencode)
      if ! command -v opencode &>/dev/null; then
        log_error "OpenCode CLI not found. Install from https://opencode.ai/docs/"
        exit 1
      fi
      ;;
    codex)
      if ! command -v codex &>/dev/null; then
        log_error "Codex CLI not found. Make sure 'codex' is in your PATH."
        exit 1
      fi
      ;;
    cursor)
      if ! command -v agent &>/dev/null; then
        log_error "Cursor agent CLI not found. Make sure Cursor is installed and 'agent' is in your PATH."
        exit 1
      fi
      ;;
    *)
      if ! command -v claude &>/dev/null; then
        log_error "Claude Code CLI not found. Install from https://github.com/anthropics/claude-code"
        exit 1
      fi
      ;;
  esac

  # Check for jq
  if ! command -v jq &>/dev/null; then
    log_warn "jq not found. Token tracking may not work properly"
  fi

  # Check for gh if PR creation is requested
  if [[ "$CREATE_PR" == true ]] && ! command -v gh &>/dev/null; then
    log_error "GitHub CLI (gh) is required for --create-pr. Install from https://cli.github.com/"
    exit 1
  fi

  # Create progress.txt if missing
  PROGRESS_FILE="$PLANS_DIR/progress.txt"
  if [[ ! -f "$PROGRESS_FILE" ]]; then
    log_warn "progress.txt not found, creating it..."
    echo "# Ralph Progress for $FEATURE_NAME" > "$PROGRESS_FILE"
    echo "" >> "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "" >> "$PROGRESS_FILE"
  fi

  # Set base branch if not specified
  if [[ "$BRANCH_PER_TASK" == true ]] && [[ -z "$BASE_BRANCH" ]]; then
    BASE_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    log_debug "Using base branch: $BASE_BRANCH"
  fi
}

# ============================================
# CLEANUP HANDLER
# ============================================

cleanup() {
  local exit_code=$?

  # Kill background processes
  [[ -n "$monitor_pid" ]] && kill "$monitor_pid" 2>/dev/null || true
  [[ -n "$ai_pid" ]] && kill "$ai_pid" 2>/dev/null || true

  # Kill parallel processes
  for pid in "${parallel_pids[@]+"${parallel_pids[@]}"}"; do
    kill "$pid" 2>/dev/null || true
  done

  # Kill any remaining child processes
  pkill -P $$ 2>/dev/null || true

  # Remove temp file
  [[ -n "$tmpfile" ]] && rm -f "$tmpfile"
  [[ -n "$CODEX_LAST_MESSAGE_FILE" ]] && rm -f "$CODEX_LAST_MESSAGE_FILE"

  # Cleanup parallel worktrees
  if [[ -n "$WORKTREE_BASE" ]] && [[ -d "$WORKTREE_BASE" ]]; then
    for dir in "$WORKTREE_BASE"/agent-*; do
      if [[ -d "$dir" ]]; then
        if git -C "$dir" status --porcelain 2>/dev/null | grep -q .; then
          log_warn "Preserving dirty worktree: $dir"
          continue
        fi
        git worktree remove "$dir" 2>/dev/null || true
      fi
    done
    if ! find "$WORKTREE_BASE" -maxdepth 1 -type d -name 'agent-*' -print -quit 2>/dev/null | grep -q .; then
      rm -rf "$WORKTREE_BASE" 2>/dev/null || true
    else
      log_warn "Preserving worktree base with dirty agents: $WORKTREE_BASE"
    fi
  fi

  # Show message on interrupt
  if [[ $exit_code -eq 130 ]]; then
    printf "\n"
    log_warn "Interrupted! Cleaned up."

    if [[ -n "${task_branches[*]+"${task_branches[*]}"}" ]]; then
      log_info "Branches created: ${task_branches[*]}"
    fi
  fi
}

# ============================================
# TASK FUNCTIONS
# ============================================

get_tasks_markdown() {
  grep '^\- \[ \]' "$PLANS_DIR/breakdown.md" 2>/dev/null | sed 's/^- \[ \] //' || true
}

get_next_task_markdown() {
  grep -m1 '^\- \[ \]' "$PLANS_DIR/breakdown.md" 2>/dev/null | sed 's/^- \[ \] //' | cut -c1-50 || echo ""
}

count_remaining_markdown() {
  grep -c '^\- \[ \]' "$PLANS_DIR/breakdown.md" 2>/dev/null || echo "0"
}

count_completed_markdown() {
  grep -c '^\- \[x\]' "$PLANS_DIR/breakdown.md" 2>/dev/null || echo "0"
}

mark_task_complete_markdown() {
  local task=$1
  local escaped_task
  escaped_task=$(printf '%s\n' "$task" | sed 's/[[\.*^$/]/\\&/g')
  sed -i.bak "s/^- \[ \] ${escaped_task}/- [x] ${escaped_task}/" "$PLANS_DIR/breakdown.md"
  rm -f "${PLANS_DIR/breakdown.md}.bak"
}

get_next_task() {
  get_next_task_markdown
}

get_all_tasks() {
  get_tasks_markdown
}

count_remaining_tasks() {
  count_remaining_markdown
}

count_completed_tasks() {
  count_completed_markdown
}

mark_task_complete() {
  local task=$1
  mark_task_complete_markdown "$task"
}

# ============================================
# GIT BRANCH MANAGEMENT
# ============================================

create_task_branch() {
  local task=$1
  local branch_name="ralph/$(slugify "$task")"

  log_debug "Creating branch: $branch_name from $BASE_BRANCH"

  local stash_before stash_after stashed=false
  stash_before=$(git stash list -1 --format='%gd %s' 2>/dev/null || true)
  git stash push -m "ralph-autostash" >/dev/null 2>&1 || true
  stash_after=$(git stash list -1 --format='%gd %s' 2>/dev/null || true)
  if [[ -n "$stash_after" ]] && [[ "$stash_after" != "$stash_before" ]] && [[ "$stash_after" == *"ralph-autostash"* ]]; then
    stashed=true
  fi

  git checkout "$BASE_BRANCH" 2>/dev/null || true
  git pull origin "$BASE_BRANCH" 2>/dev/null || true
  git checkout -b "$branch_name" 2>/dev/null || {
    git checkout "$branch_name" 2>/dev/null || true
  }

  if [[ "$stashed" == true ]]; then
    git stash pop >/dev/null 2>&1 || true
  fi

  task_branches+=("$branch_name")
  echo "$branch_name"
}

create_pull_request() {
  local branch=$1
  local task=$2
  local body="${3:-Automated PR created by Ralph}"

  local draft_flag=""
  [[ "$PR_DRAFT" == true ]] && draft_flag="--draft"

  log_info "Creating pull request for $branch..."

  git push -u origin "$branch" 2>/dev/null || {
    log_warn "Failed to push branch $branch"
    return 1
  }

  local pr_url
  pr_url=$(gh pr create \
    --base "$BASE_BRANCH" \
    --head "$branch" \
    --title "$task" \
    --body "$body" \
    $draft_flag 2>/dev/null) || {
    log_warn "Failed to create PR for $branch"
    return 1
  }

  log_success "PR created: $pr_url"
  echo "$pr_url"
}

return_to_base_branch() {
  if [[ "$BRANCH_PER_TASK" == true ]]; then
    git checkout "$BASE_BRANCH" 2>/dev/null || true
  fi
}

# ============================================
# PROGRESS MONITOR
# ============================================

monitor_progress() {
  local file=$1
  local task=$2
  local start_time
  start_time=$(date +%s)
  local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  local spin_idx=0

  task="${task:0:40}"

  while true; do
    local elapsed=$(($(date +%s) - start_time))
    local mins=$((elapsed / 60))
    local secs=$((elapsed % 60))

    if [[ -f "$file" ]] && [[ -s "$file" ]]; then
      local content
      content=$(tail -c 5000 "$file" 2>/dev/null || true)

      if echo "$content" | grep -qE 'git commit|"command":"git commit'; then
        current_step="Committing"
      elif echo "$content" | grep -qE 'git add|"command":"git add'; then
        current_step="Staging"
      elif echo "$content" | grep -qE 'lint|eslint|biome|prettier'; then
        current_step="Linting"
      elif echo "$content" | grep -qE 'vitest|jest|bun test|npm test|pytest|go test'; then
        current_step="Testing"
      elif echo "$content" | grep -qE '\.test\.|\.spec\.|__tests__|_test\.go'; then
        current_step="Writing tests"
      elif echo "$content" | grep -qE '"tool":"[Ww]rite"|"tool":"[Ee]dit"|"name":"write"|"name":"edit"'; then
        current_step="Implementing"
      elif echo "$content" | grep -qE '"tool":"[Rr]ead"|"tool":"[Gg]lob"|"tool":"[Gg]rep"|"name":"read"|"name":"glob"|"name":"grep"'; then
        current_step="Reading code"
      fi
    fi

    local spinner_char="${spinstr:$spin_idx:1}"
    local step_color=""

    case "$current_step" in
      "Thinking"|"Reading code") step_color="$CYAN" ;;
      "Implementing"|"Writing tests") step_color="$MAGENTA" ;;
      "Testing"|"Linting") step_color="$YELLOW" ;;
      "Staging"|"Committing") step_color="$GREEN" ;;
      *) step_color="$BLUE" ;;
    esac

    tput cr 2>/dev/null || printf "\r"
    tput el 2>/dev/null || true
    printf "  %s ${step_color}%-16s${RESET} │ %s ${DIM}[%02d:%02d]${RESET}" "$spinner_char" "$current_step" "$task" "$mins" "$secs"

    spin_idx=$(( (spin_idx + 1) % ${#spinstr} ))
    sleep 0.12
  done
}

# ============================================
# PROMPT BUILDER
# ============================================

build_prompt() {
  local task_override="${1:-}"
  local prompt="@$PLANS_DIR/breakdown.md @$PLANS_DIR/progress.txt"

  if [[ -f "$PLANS_DIR/design.md" ]]; then
    prompt="$prompt @$PLANS_DIR/design.md"
  fi

  prompt="$prompt

1. Find the highest-priority incomplete task and implement it."

  local step=2

  if [[ "$SKIP_TESTS" == false ]]; then
    prompt="$prompt
$step. Write tests for the feature.
$((step+1)). Run tests and ensure they pass before proceeding."
    step=$((step+2))
  fi

  if [[ "$SKIP_LINT" == false ]]; then
    prompt="$prompt
$step. Run linting and ensure it passes before proceeding."
    step=$((step+1))
  fi

  prompt="$prompt
$step. Update the breakdown to mark the task as complete (change '- [ ]' to '- [x]')."
  step=$((step+1))

  prompt="$prompt
$step. Append your progress to progress.txt.
$((step+1)). Commit your changes with a descriptive message.
ONLY WORK ON A SINGLE TASK."

  if [[ "$SKIP_TESTS" == false ]]; then
    prompt="$prompt Do not proceed if tests fail."
  fi
  if [[ "$SKIP_LINT" == false ]]; then
    prompt="$prompt Do not proceed if linting fails."
  fi

  prompt="$prompt
If ALL tasks in the breakdown are complete, output <promise>COMPLETE</promise>."

  echo "$prompt"
}

# ============================================
# AI ENGINE ABSTRACTION
# ============================================

run_ai_command() {
  local prompt=$1
  local output_file=$2

  case "$AI_ENGINE" in
    opencode)
      OPENCODE_PERMISSION='{"*":"allow"}' opencode run \
        --format json \
        "$prompt" > "$output_file" 2>&1 &
      ;;
    cursor)
      agent --print --force \
        --output-format stream-json \
        "$prompt" > "$output_file" 2>&1 &
      ;;
    codex)
      CODEX_LAST_MESSAGE_FILE="${output_file}.last"
      rm -f "$CODEX_LAST_MESSAGE_FILE"
      codex exec --full-auto \
        --json \
        --output-last-message "$CODEX_LAST_MESSAGE_FILE" \
        "$prompt" > "$output_file" 2>&1 &
      ;;
    *)
      claude --dangerously-skip-permissions \
        --verbose \
        --output-format stream-json \
        -p "$prompt" > "$output_file" 2>&1 &
      ;;
  esac

  ai_pid=$!
}

parse_ai_result() {
  local result=$1
  local response=""
  local input_tokens=0
  local output_tokens=0
  local actual_cost="0"

  case "$AI_ENGINE" in
    opencode)
      local step_finish
      step_finish=$(echo "$result" | grep '"type":"step_finish"' | tail -1 || echo "")

      if [[ -n "$step_finish" ]]; then
        input_tokens=$(echo "$step_finish" | jq -r '.part.tokens.input // 0' 2>/dev/null || echo "0")
        output_tokens=$(echo "$step_finish" | jq -r '.part.tokens.output // 0' 2>/dev/null || echo "0")
        actual_cost=$(echo "$step_finish" | jq -r '.part.cost // 0' 2>/dev/null || echo "0")
      fi

      response=$(echo "$result" | grep '"type":"text"' | jq -rs 'map(.part.text // "") | join("")' 2>/dev/null || echo "")

      if [[ -z "$response" ]]; then
        response="Task completed"
      fi
      ;;
    cursor)
      local result_line
      result_line=$(echo "$result" | grep '"type":"result"' | tail -1)

      if [[ -n "$result_line" ]]; then
        response=$(echo "$result_line" | jq -r '.result // "Task completed"' 2>/dev/null || echo "Task completed")
        local duration_ms
        duration_ms=$(echo "$result_line" | jq -r '.duration_ms // 0' 2>/dev/null || echo "0")
        if [[ "$duration_ms" =~ ^[0-9]+$ ]] && [[ "$duration_ms" -gt 0 ]]; then
          actual_cost="duration:$duration_ms"
        fi
      fi

      if [[ -z "$response" ]] || [[ "$response" == "Task completed" ]]; then
        local assistant_msg
        assistant_msg=$(echo "$result" | grep '"type":"assistant"' | tail -1)
        if [[ -n "$assistant_msg" ]]; then
          response=$(echo "$assistant_msg" | jq -r '.message.content[0].text // .message.content // "Task completed"' 2>/dev/null || echo "Task completed")
        fi
      fi

      input_tokens=0
      output_tokens=0
      ;;
    codex)
      if [[ -n "$CODEX_LAST_MESSAGE_FILE" ]] && [[ -f "$CODEX_LAST_MESSAGE_FILE" ]]; then
        response=$(cat "$CODEX_LAST_MESSAGE_FILE" 2>/dev/null || echo "")
        response=$(printf '%s' "$response" | sed '1{/^Task completed successfully\.[[:space:]]*$/d;}')
      fi
      input_tokens=0
      output_tokens=0
      ;;
    *)
      local result_line
      result_line=$(echo "$result" | grep '"type":"result"' | tail -1)

      if [[ -n "$result_line" ]]; then
        response=$(echo "$result_line" | jq -r '.result // "No result text"' 2>/dev/null || echo "Could not parse result")
        input_tokens=$(echo "$result_line" | jq -r '.usage.input_tokens // 0' 2>/dev/null || echo "0")
        output_tokens=$(echo "$result_line" | jq -r '.usage.output_tokens // 0' 2>/dev/null || echo "0")
      fi
      ;;
  esac

  [[ "$input_tokens" =~ ^[0-9]+$ ]] || input_tokens=0
  [[ "$output_tokens" =~ ^[0-9]+$ ]] || output_tokens=0

  echo "$response"
  echo "---TOKENS---"
  echo "$input_tokens"
  echo "$output_tokens"
  echo "$actual_cost"
}

check_for_errors() {
  local result=$1

  if echo "$result" | grep -q '"type":"error"'; then
    local error_msg
    error_msg=$(echo "$result" | grep '"type":"error"' | head -1 | jq -r '.error.message // .message // .' 2>/dev/null || echo "Unknown error")
    echo "$error_msg"
    return 1
  fi

  return 0
}

# ============================================
# COST CALCULATION
# ============================================

calculate_cost() {
  local input=$1
  local output=$2

  if command -v bc &>/dev/null; then
    echo "scale=4; ($input * 0.000003) + ($output * 0.000015)" | bc
  else
    echo "N/A"
  fi
}

# ============================================
# SINGLE TASK EXECUTION
# ============================================

run_single_task() {
  local task_name="${1:-}"
  local task_num="${2:-$iteration}"

  retry_count=0

  echo ""
  echo "${BOLD}>>> Task $task_num${RESET}"

  local remaining completed
  remaining=$(count_remaining_tasks | tr -d '[:space:]')
  completed=$(count_completed_tasks | tr -d '[:space:]')
  remaining=${remaining:-0}
  completed=${completed:-0}
  echo "${DIM}    Completed: $completed | Remaining: $remaining${RESET}"
  echo "--------------------------------------------"

  local current_task
  if [[ -n "$task_name" ]]; then
    current_task="$task_name"
  else
    current_task=$(get_next_task)
  fi

  if [[ -z "$current_task" ]]; then
    log_info "No more tasks found"
    return 2
  fi

  current_step="Thinking"

  local branch_name=""
  if [[ "$BRANCH_PER_TASK" == true ]]; then
    branch_name=$(create_task_branch "$current_task")
    log_info "Working on branch: $branch_name"
  fi

  tmpfile=$(mktemp)

  local prompt
  prompt=$(build_prompt "$current_task")

  if [[ "$DRY_RUN" == true ]]; then
    log_info "DRY RUN - Would execute:"
    echo "${DIM}$prompt${RESET}"
    rm -f "$tmpfile"
    tmpfile=""
    return_to_base_branch
    return 0
  fi

  while [[ $retry_count -lt $MAX_RETRIES ]]; do
    run_ai_command "$prompt" "$tmpfile"

    monitor_progress "$tmpfile" "${current_task:0:40}" &
    monitor_pid=$!

    wait "$ai_pid" 2>/dev/null || true

    kill "$monitor_pid" 2>/dev/null || true
    wait "$monitor_pid" 2>/dev/null || true
    monitor_pid=""

    tput cr 2>/dev/null || printf "\r"
    tput el 2>/dev/null || true

    local result
    result=$(cat "$tmpfile" 2>/dev/null || echo "")

    if [[ -z "$result" ]]; then
      ((retry_count++))
      log_error "Empty response (attempt $retry_count/$MAX_RETRIES)"
      if [[ $retry_count -lt $MAX_RETRIES ]]; then
        log_info "Retrying in ${RETRY_DELAY}s..."
        sleep "$RETRY_DELAY"
        continue
      fi
      rm -f "$tmpfile"
      tmpfile=""
      return_to_base_branch
      return 1
    fi

    local error_msg
    if ! error_msg=$(check_for_errors "$result"); then
      ((retry_count++))
      log_error "API error: $error_msg (attempt $retry_count/$MAX_RETRIES)"
      if [[ $retry_count -lt $MAX_RETRIES ]]; then
        log_info "Retrying in ${RETRY_DELAY}s..."
        sleep "$RETRY_DELAY"
        continue
      fi
      rm -f "$tmpfile"
      tmpfile=""
      return_to_base_branch
      return 1
    fi

    local parsed
    parsed=$(parse_ai_result "$result")
    local response
    response=$(echo "$parsed" | sed '/^---TOKENS---$/,$d')
    local token_data
    token_data=$(echo "$parsed" | sed -n '/^---TOKENS---$/,$p' | tail -3)
    local input_tokens
    input_tokens=$(echo "$token_data" | sed -n '1p')
    local output_tokens
    output_tokens=$(echo "$token_data" | sed -n '2p')
    local actual_cost
    actual_cost=$(echo "$token_data" | sed -n '3p')

    printf "  ${GREEN}✓${RESET} %-16s │ %s\n" "Done" "${current_task:0:40}"

    if [[ -n "$response" ]]; then
      echo ""
      echo "$response"
    fi

    [[ "$input_tokens" =~ ^[0-9]+$ ]] || input_tokens=0
    [[ "$output_tokens" =~ ^[0-9]+$ ]] || output_tokens=0

    total_input_tokens=$((total_input_tokens + input_tokens))
    total_output_tokens=$((total_output_tokens + output_tokens))

    if [[ -n "$actual_cost" ]]; then
      if [[ "$actual_cost" == duration:* ]]; then
        local dur_ms="${actual_cost#duration:}"
        [[ "$dur_ms" =~ ^[0-9]+$ ]] && total_duration_ms=$((total_duration_ms + dur_ms))
      elif [[ "$actual_cost" != "0" ]] && command -v bc &>/dev/null; then
        total_actual_cost=$(echo "scale=6; $total_actual_cost + $actual_cost" | bc 2>/dev/null || echo "$total_actual_cost")
      fi
    fi

    rm -f "$tmpfile"
    tmpfile=""
    if [[ "$AI_ENGINE" == "codex" ]] && [[ -n "$CODEX_LAST_MESSAGE_FILE" ]]; then
      rm -f "$CODEX_LAST_MESSAGE_FILE"
      CODEX_LAST_MESSAGE_FILE=""
    fi

    if [[ "$CREATE_PR" == true ]] && [[ -n "$branch_name" ]]; then
      create_pull_request "$branch_name" "$current_task" "Automated implementation by Ralph"
    fi

    return_to_base_branch

    local remaining_count
    remaining_count=$(count_remaining_tasks | tr -d '[:space:]' | head -1)
    remaining_count=${remaining_count:-0}
    [[ "$remaining_count" =~ ^[0-9]+$ ]] || remaining_count=0

    if [[ "$remaining_count" -eq 0 ]]; then
      return 2
    fi

    if [[ "$result" == *"<promise>COMPLETE</promise>"* ]]; then
      log_debug "AI claimed completion but $remaining_count tasks remain, continuing..."
    fi

    return 0
  done

  return_to_base_branch
  return 1
}

# ============================================
# SUMMARY
# ============================================

show_summary() {
  echo ""
  echo "${BOLD}============================================${RESET}"
  echo "${GREEN}PRD complete!${RESET} Finished $iteration task(s)."
  echo "${BOLD}============================================${RESET}"
  echo ""
  echo "${BOLD}>>> Cost Summary${RESET}"

  if [[ "$AI_ENGINE" == "cursor" ]]; then
    echo "${DIM}Token usage not available (Cursor CLI doesn't expose this data)${RESET}"
    if [[ "$total_duration_ms" -gt 0 ]]; then
      local dur_sec=$((total_duration_ms / 1000))
      local dur_min=$((dur_sec / 60))
      local dur_sec_rem=$((dur_sec % 60))
      if [[ "$dur_min" -gt 0 ]]; then
        echo "Total API time: ${dur_min}m ${dur_sec_rem}s"
      else
        echo "Total API time: ${dur_sec}s"
      fi
    fi
  else
    echo "Input tokens:  $total_input_tokens"
    echo "Output tokens: $total_output_tokens"
    echo "Total tokens:  $((total_input_tokens + total_output_tokens))"

    if [[ "$AI_ENGINE" == "opencode" ]] && command -v bc &>/dev/null; then
      local has_actual_cost
      has_actual_cost=$(echo "$total_actual_cost > 0" | bc 2>/dev/null || echo "0")
      if [[ "$has_actual_cost" == "1" ]]; then
        echo "Actual cost:   \$${total_actual_cost}"
      else
        local cost
        cost=$(calculate_cost "$total_input_tokens" "$total_output_tokens")
        echo "Est. cost:     \$$cost"
      fi
    else
      local cost
      cost=$(calculate_cost "$total_input_tokens" "$total_output_tokens")
      echo "Est. cost:     \$$cost"
    fi
  fi

  if [[ -n "${task_branches[*]+"${task_branches[*]}"}" ]]; then
    echo ""
    echo "${BOLD}>>> Branches Created${RESET}"
    for branch in "${task_branches[@]}"; do
      echo "  - $branch"
    done
  fi

  echo "${BOLD}============================================${RESET}"
}

# ============================================
# MAIN
# ============================================

main() {
  parse_args "$@"

  # Exit early if showing help/version
  if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]] || [[ "$1" == "--version" ]]; then
    return 0
  fi

  check_requirements

  if [[ "$DRY_RUN" == true ]] && [[ "$MAX_ITERATIONS" -eq 0 ]]; then
    MAX_ITERATIONS=1
  fi

  trap cleanup EXIT
  trap 'exit 130' INT TERM HUP

  echo "${BOLD}============================================${RESET}"
  echo "${BOLD}Ralph Loop${RESET} - Running until breakdown is complete"
  local engine_display
  case "$AI_ENGINE" in
    opencode) engine_display="${CYAN}OpenCode${RESET}" ;;
    cursor) engine_display="${YELLOW}Cursor Agent${RESET}" ;;
    codex) engine_display="${BLUE}Codex${RESET}" ;;
    *) engine_display="${MAGENTA}Claude Code${RESET}" ;;
  esac
  echo "Engine: $engine_display"
  echo "Feature: ${CYAN}$FEATURE_NAME${RESET}"

  local mode_parts=()
  [[ "$SKIP_TESTS" == true ]] && mode_parts+=("no-tests")
  [[ "$SKIP_LINT" == true ]] && mode_parts+=("no-lint")
  [[ "$DRY_RUN" == true ]] && mode_parts+=("dry-run")
  [[ "$BRANCH_PER_TASK" == true ]] && mode_parts+=("branch-per-task")
  [[ "$CREATE_PR" == true ]] && mode_parts+=("create-pr")
  [[ $MAX_ITERATIONS -gt 0 ]] && mode_parts+=("max:$MAX_ITERATIONS")

  if [[ ${#mode_parts[@]} -gt 0 ]]; then
    echo "Mode: ${YELLOW}${mode_parts[*]}${RESET}"
  fi
  echo "${BOLD}============================================${RESET}"

  if [[ "$PARALLEL" == true ]]; then
    log_warn "Parallel execution not yet implemented, running sequentially"
  fi

  while true; do
    ((iteration++))
    local result_code=0
    run_single_task "" "$iteration" || result_code=$?

    case $result_code in
      0)
        ;;
      1)
        log_warn "Task failed after $MAX_RETRIES attempts, continuing..."
        ;;
      2)
        show_summary
        exit 0
        ;;
    esac

    if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $iteration -ge $MAX_ITERATIONS ]]; then
      log_warn "Reached max iterations ($MAX_ITERATIONS)"
      show_summary
      exit 0
    fi

    sleep 1
  done
}

main "$@"
