#!/bin/zsh
# Ralph Loop - Autonomous Implementation for Claude Code Lifecycle
# Usage: ./ralph-loop.sh <feature-name> [max-iterations] [sleep-seconds]

set -e

FEATURE_NAME=${1}
MAX=${2:-10}
SLEEP=${3:-2}
PLANS_DIR="plans/${FEATURE_NAME}"

if [ -z "$FEATURE_NAME" ]; then
    echo "❌ Error: Feature name required"
    echo "Usage: ./ralph-loop.sh <feature-name> [max-iterations] [sleep-seconds]"
    echo ""
    echo "Example:"
    echo "  ./ralph-loop.sh 'User Authentication' 20 3"
    exit 1
fi

if [ ! -d "$PLANS_DIR" ]; then
    echo "❌ Error: Plans directory not found: $PLANS_DIR"
    echo "Please run /breakdown first to create the plan structure"
    exit 1
fi

echo "🚀 Starting Ralph Loop"
echo "================================"
echo "Feature: $FEATURE_NAME"
echo "Max Iterations: $MAX"
echo "Sleep: ${SLEEP}s between iterations"
echo "Plans Directory: $PLANS_DIR"
echo "================================"
echo ""

# Create progress.txt if it doesn't exist
PROGRESS_FILE="$PLANS_DIR/progress.txt"
if [ ! -f "$PROGRESS_FILE" ]; then
    echo "# Ralph Progress for $FEATURE_NAME" > "$PROGRESS_FILE"
    echo "" >> "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "" >> "$PROGRESS_FILE"
fi

for ((i=1; i<=$MAX; i++)); do
    echo "==========================================="
    echo "  🔄 Iteration $i of $MAX"
    echo "==========================================="
    echo ""

    result=$(claude --dangerously-skip-permissions -p "You are Ralph, an autonomous coding agent implementing the $FEATURE_NAME feature.

## Your Task

Do exactly ONE story/task per iteration following the lifecycle approach.

## Steps

1. **Read Progress First**
   Read \`$PROGRESS_FILE\` - check the most recent iteration for:
   - What worked in previous iterations
   - Patterns discovered
   - Gotchas encountered
   - Learnings to apply

2. **Find Next Task**
   Read \`$PLANS_DIR/breakdown.md\`
   - Find the first story marked with [ ] (incomplete)
   - Note the story ID and description

3. **Read Design**
   Read the technical design:
   - Check \`$PLANS_DIR/design.md\` for epic-level design
   - Check \`$PLANS_DIR/stories/{story-id}.md\` for story-specific design
   - Understand the architecture, patterns, and approach

4. **Implement Story**
   Follow the implementation guidelines from \`$PLANS_DIR/implement.md\`:
   - Create/modify files as designed
   - Handle edge cases identified in design
   - Follow file structure preferences
   - Write tests as specified

5. **Verify It Works**
   - Run the test suite
   - Run type checking (if applicable)
   - Run linting (if applicable)
   - Ensure all tests pass

## Critical: Only Complete If Tests Pass

✅ **If tests PASS**:
   - Update \`$PLANS_DIR/breakdown.md\` to mark the story complete (change [ ] to [x])
   - Commit your changes with message: \`feat: [story description]\`
   - Append to \`$PROGRESS_FILE\` using this format:

\`\`\`
## Iteration $i - [Story ID]: [Story Name]
- Status: ✅ Complete
- Files changed:
  - path/to/file1.ext (new/modified)
  - path/to/file2.ext (new/modified)
- Commit: feat: [commit message]
- Learnings:
  - [Pattern discovered]
  - [Gotcha encountered]
  - [Useful context for next iterations]
\`\`\`

❌ **If tests FAIL**:
   - Do NOT mark the story complete
   - Do NOT commit broken code
   - Append to \`$PROGRESS_FILE\` what went wrong
   - End your response (next iteration will retry)

## End Condition

After completing your task:
- Read \`$PLANS_DIR/breakdown.md\`
- If ALL stories are marked [x], output exactly: \`<promise>COMPLETE</promise>\`
- If stories remain [ ], just end your response

## Important

- Follow the design document exactly
- Use the file structure specified in design
- Handle all edge cases mentioned in design
- Match the coding style of existing codebase
- Keep commits focused and atomic
- Learn from previous iterations' progress")

    echo "$result"
    echo ""

    # Update progress file with iteration separator
    echo "" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
    echo "Iteration $i completed at $(date)" >> "$PROGRESS_FILE"
    echo "" >> "$PROGRESS_FILE"

    if [[ "$result" == *"<promise>COMPLETE</promise>"* ]]; then
        echo "==========================================="
        echo "  ✅ All stories complete after $i iterations!"
        echo "==========================================="
        echo ""
        echo "📊 Final Progress:"
        cat "$PROGRESS_FILE"
        exit 0
    fi

    if [ $i -lt $MAX ]; then
        echo "⏳ Sleeping ${SLEEP}s before next iteration..."
        sleep $SLEEP
    fi
done

echo "==========================================="
echo "  ⚠️  Reached max iterations ($MAX)"
echo "==========================================="
echo ""
echo "📊 Current Progress:"
cat "$PROGRESS_FILE"
echo ""
echo "💡 To continue, run:"
echo "  ./ralph-loop.sh \"$FEATURE_NAME\" $MAX $SLEEP"
exit 1
