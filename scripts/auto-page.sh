#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
[[ ${DEBUG:-} == true ]] && set -o xtrace

# Simple pager: Uses 'head' and 'tail' to auto-page through file
# This shows a new "page" every 5 seconds

FILE="${1:-}"
if [[ -z "$FILE" ]]; then
    echo "Usage: $0 <file> [window] [sleep]"
    exit 1
fi

declare -i WINDOW=${2:-138}
declare -i SLEEP=${3:-5}
declare -i LINE=0
declare -i TOTAL
TOTAL=$(wc -l < "$FILE")

while [ $LINE -lt $TOTAL ]; do
    clear
    echo "=== Lines $((LINE + 1)) to $((LINE + WINDOW)) of $TOTAL ==="
    { tail -n +$((LINE + 1)) "$FILE" | head -n $WINDOW; } || true
    LINE=$((LINE + WINDOW))
    # Use sleep with error handling - continue even if interrupted
    sleep $SLEEP 2>/dev/null || true
done
