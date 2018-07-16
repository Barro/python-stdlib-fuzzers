#!/usr/bin/env bash

set -euo pipefail

TARGET=$1
PYTHON_CMD=${PYTHON_CMD:-python3}

TARGET_SCRIPT=$TARGET/fuzz.py
if ! [[ -f "$TARGET_SCRIPT" ]]; then
    echo >&2 "Fuzz target $TARGET/fuzz.py does not exist!"
    exit 1
fi

# Regression test data is in the order of failure probability finding
# directories. Meaning that if the directory that comes up in this
# list has failures, likely the next directory has the same failures.
CHECK_DIRS=(
    "$TARGET"/in
    "$TARGET"/corpus
    "$TARGET"/crashes
    "$TARGET"/crashes-raw
)

echo >&2 "Running regression tests for $TARGET"

last_directory=
failures=0
exit_code=0
for dir in "${CHECK_DIRS[@]}"; do
    last_directory=$dir
    if [[ ! -d "$dir" ]]; then
        continue
    fi
    files=$(find "$dir" -type f)
    while read -r filename; do
        (ulimit -v 200000; "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename" 1>/dev/null 2>/dev/null) && continue
        exit_code=1
        failures=$(( failures + 1 ))
        (ulimit -v 200000; "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename") || :
        echo "$filename"
    done <<< "$files"
    # Abort on the first failing directory, as further processing
    # would likely just reveal duplicates of previous issues:
    if [[ "$exit_code" -ne 0 ]]; then
        break
    fi
done

if [[ "$exit_code" -ne 0 ]]; then
    echo "Detected $failures failing files at $last_directory/ directory!"
fi

exit "$exit_code"
