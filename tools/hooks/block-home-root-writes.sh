#!/bin/bash
# Blocks agent sessions from creating new files or dirs directly at $HOME top level.
# Targets agent tool calls only (Write/Bash via Claude Code hooks) - never touches
# anything Mike does himself outside a session. Deliberate bypass: one-shot flag file.

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
BYPASS_FLAG="$HOME/.claude/.allow-home-root-write"
DEST_HINT="the task OUTPUT destination: its owning repository docs or runtime task directory"

block_or_bypass() {
  local target="$1"
  if [ -f "$BYPASS_FLAG" ]; then
    rm -f "$BYPASS_FLAG"
    echo "ALLOWED (one-shot bypass consumed): $target" >&2
    return 0
  fi
  {
    echo "BLOCKED: agent sessions may not create new files or directories directly at"
    echo "$HOME top level ($target)."
    echo "Put it in $DEST_HINT instead."
    echo "If Mike explicitly wants this exact path, run: touch $BYPASS_FLAG"
    echo "(one-shot: the flag clears itself the moment it is used, so it cannot be left on by accident)."
  } >&2
  exit 2
}

case "$TOOL" in
  Write|NotebookEdit)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    [ -z "$FILE_PATH" ] && exit 0
    case "$FILE_PATH" in
      "$HOME"/*) : ;;
      "~/"*) FILE_PATH="$HOME/${FILE_PATH#\~/}" ;;
      *) exit 0 ;;
    esac
    DIRNAME=$(dirname "$FILE_PATH")
    BASENAME=$(basename "$FILE_PATH")
    if [ "$DIRNAME" = "$HOME" ]; then
      case "$BASENAME" in
        .*) exit 0 ;;
      esac
      block_or_bypass "$FILE_PATH"
    fi
    exit 0
    ;;
  Bash)
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
    [ -z "$COMMAND" ] && exit 0
    if echo "$COMMAND" | grep -qE '(^|[;&|]|[[:space:]])(>{1,2}|touch|mkdir([[:space:]]+-p)?)[[:space:]]+("?(~|\$HOME)"?|/Users/man)/[^/[:space:]"'\'']+([[:space:]]|["'\'']?$|["'\''<])'; then
      block_or_bypass "(bash) $COMMAND"
    fi
    if echo "$COMMAND" | grep -qE '\b(mv|cp)\b.*[[:space:]]("?(~|\$HOME)"?|/Users/man)/?[[:space:]]*$'; then
      block_or_bypass "(bash) $COMMAND"
    fi
    exit 0
    ;;
  *)
    exit 0
    ;;
esac
