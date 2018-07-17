#!/usr/bin/env bash

set -euo pipefail

TARGET=$1
PYTHON_CMD=${PYTHON_CMD:-python3}

TARGET_SCRIPT=$TARGET/fuzz.py
if ! [[ -f "$TARGET_SCRIPT" ]]; then
    echo >&2 "Fuzz target $TARGET/fuzz.py does not exist!"
    exit 1
fi
OUTDIR=/dev/shm/python-stdlib-$TARGET

crashes=$(find "$OUTDIR" -type f | grep crashes/id | sort || :)
if [[ -z "$crashes" ]]; then
    echo >&2 "No crashes found for $TARGET"
    exit 0
fi

echo >&2 "Running $TARGET with $PYTHON_CMD"

while read -r filename; do
    (ulimit -v 200000; "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename") && continue
    (ulimit -v 200000; "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename" 1>/dev/null 2>"$OUTDIR"/current-crash) || :
    echo >&2 "$PYTHON_CMD" "$TARGET_SCRIPT" "$filename"
    ./normalize-backtrace.py < "$OUTDIR"/current-crash > "$OUTDIR"/current-crash.normalized
    read -r stack_trace_sum _ <<< "$(sha256sum -b "$OUTDIR"/current-crash.normalized)"
    mkdir -p "$TARGET"/crashes-raw
    cp "$filename" "$TARGET"/crashes-raw/"$stack_trace_sum".in
    cp "$OUTDIR"/current-crash.normalized "$TARGET"/crashes-raw/backtrace."$stack_trace_sum".txt
done <<< "$crashes"
